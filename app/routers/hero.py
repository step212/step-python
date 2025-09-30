from typing import Annotated
from fastapi import APIRouter, Query
from app.models.hero import Hero, HeroCreate, HeroPublic, HeroUpdate
from app.biz.hero import HeroBiz
from app.dependencies import HeroBizDep

router = APIRouter(
    prefix="/heros",
    tags=["heros"],
)

@router.post("/", response_model=HeroPublic)
async def create_hero(hero: HeroCreate, biz: HeroBizDep) -> HeroPublic:
    return await biz.create_hero(hero)

@router.get("/", response_model=list[HeroPublic])
async def read_heroes(biz: HeroBizDep, page: int = 1, page_size: Annotated[int, Query(le=100)] = 10) -> list[HeroPublic]:
    return await biz.get_heroes(page, page_size)

@router.get("/{hero_id}", response_model=Hero)
async def read_hero(hero_id: int, biz: HeroBizDep) -> Hero:
    return await biz.get_hero(hero_id)

@router.patch("/{hero_id}", response_model=HeroPublic)
async def update_hero(hero_id: int, hero: HeroUpdate, biz: HeroBizDep) -> HeroPublic:
    return await biz.update_hero(hero_id, hero)

@router.delete("/{hero_id}")
async def delete_hero(hero_id: int, biz: HeroBizDep) -> dict:
    return await biz.delete_hero(hero_id)