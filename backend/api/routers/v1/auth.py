"""Auth endpoints: /api/v1/auth/*."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.deps import ClientContext, JwtUser, get_client_context, get_jwt_user
from backend.db.session import get_async_session
from backend.services.auth_service import (
    create_invite_code_for_parent,
    create_web_code_for_student,
    exchange_invite_code,
    exchange_student_code,
    get_student_for_user,
    get_user_role,
)
from backend.services.identity import get_or_create_student
from backend.services.jwt_service import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
)

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    code: str = Field(..., min_length=1)


class InviteAcceptRequest(BaseModel):
    code: str = Field(..., min_length=1)
    display_name: str = Field(..., min_length=1)


class RefreshRequest(BaseModel):
    refresh_token: str


class AuthUserResponse(BaseModel):
    user_id: int
    role: str
    display_name: str
    student_id: int | None = None


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: AuthUserResponse


@router.post("/login", response_model=TokenResponse)
async def login_with_code(
    body: LoginRequest,
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> TokenResponse:
    result = await exchange_student_code(session, body.code.strip())
    if result is None:
        raise HTTPException(status_code=401, detail="Invalid or expired code")
    user, student, role = result
    await session.commit()

    access = create_access_token(user.id, role)
    refresh = create_refresh_token(user.id)
    return TokenResponse(
        access_token=access,
        refresh_token=refresh,
        user=AuthUserResponse(
            user_id=user.id,
            role=role,
            display_name=student.display_name,
            student_id=student.id,
        ),
    )


@router.post("/accept-invite", response_model=TokenResponse)
async def accept_invite(
    body: InviteAcceptRequest,
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> TokenResponse:
    result = await exchange_invite_code(session, body.code.strip(), body.display_name.strip())
    if result is None:
        raise HTTPException(status_code=401, detail="Invalid or expired invite code")
    user, role = result
    await session.commit()

    access = create_access_token(user.id, role)
    refresh = create_refresh_token(user.id)
    return TokenResponse(
        access_token=access,
        refresh_token=refresh,
        user=AuthUserResponse(
            user_id=user.id,
            role=role,
            display_name=body.display_name.strip(),
        ),
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_tokens(
    body: RefreshRequest,
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> TokenResponse:
    payload = decode_refresh_token(body.refresh_token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user_id = int(payload["sub"])
    role = await get_user_role(session, user_id)
    student = await get_student_for_user(session, user_id)

    display_name = student.display_name if student else f"user:{user_id}"
    access = create_access_token(user_id, role)
    refresh = create_refresh_token(user_id)
    return TokenResponse(
        access_token=access,
        refresh_token=refresh,
        user=AuthUserResponse(
            user_id=user_id,
            role=role,
            display_name=display_name,
            student_id=student.id if student else None,
        ),
    )


@router.get("/me", response_model=AuthUserResponse)
async def get_current_user(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    jwt_user: Annotated[JwtUser, Depends(get_jwt_user)],
) -> AuthUserResponse:
    student = await get_student_for_user(session, jwt_user.user_id)
    display_name = student.display_name if student else f"user:{jwt_user.user_id}"
    return AuthUserResponse(
        user_id=jwt_user.user_id,
        role=jwt_user.role,
        display_name=display_name,
        student_id=student.id if student else None,
    )


class CodeResponse(BaseModel):
    code: str


@router.post("/web-code", response_model=CodeResponse)
async def generate_web_code(
    ctx: Annotated[ClientContext, Depends(get_client_context)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> CodeResponse:
    """Generate a one-time code for student web login (called by bot)."""
    student = await get_or_create_student(session, ctx.channel, ctx.external_user_id)
    code = await create_web_code_for_student(session, student.user_id, student.id)
    await session.commit()
    return CodeResponse(code=code)


@router.post("/invite-code", response_model=CodeResponse)
async def generate_invite_code(
    ctx: Annotated[ClientContext, Depends(get_client_context)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> CodeResponse:
    """Generate a parent invite code (called by bot on behalf of a student)."""
    student = await get_or_create_student(session, ctx.channel, ctx.external_user_id)
    code = await create_invite_code_for_parent(session, student.id)
    await session.commit()
    return CodeResponse(code=code)
