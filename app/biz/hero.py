from fastapi import HTTPException
from app.models.hero import Hero, HeroCreate, HeroUpdate, HeroPublic
from app.data.hero import HeroData

class HeroBiz:
    def __init__(self):
        self.hero_data = HeroData()

    async def create_hero(self, hero: HeroCreate) -> HeroPublic:
        # Convert HeroCreate to Hero
        hero_data = Hero.model_validate(hero.model_dump())
        db_hero = await self.hero_data.create(hero_data)
        return HeroPublic.model_validate(db_hero)

    async def get_heroes(self, page: int = 1, page_size: int = 10) -> list[HeroPublic]:
        heroes = await self.hero_data.get_all(page, page_size)
        return [HeroPublic.model_validate(hero) for hero in heroes]

    async def get_hero(self, hero_id: int) -> Hero:
        hero = await self.hero_data.get_by_id(hero_id)
        if not hero:
            raise HTTPException(status_code=404, detail="Hero not found")
        return hero

    async def update_hero(self, hero_id: int, hero: HeroUpdate) -> HeroPublic: 
        # First get the existing hero
        existing_hero = await self.get_hero(hero_id)
        
        # Update only the fields that are provided
        update_data = hero.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(existing_hero, field, value)
            
        updated_hero = await self.hero_data.update(existing_hero)
        return HeroPublic.model_validate(updated_hero)

    async def delete_hero(self, hero_id: int) -> dict:
        if not await self.hero_data.delete(hero_id):
            raise HTTPException(status_code=404, detail="Hero not found")
        return True