from sqlmodel import select
from app.models.hero import Hero
from app.data.db import get_db
from typing import Union

class HeroData:
    def __init__(self):
        self.session = next(get_db())

    async def create(self, hero: Hero) -> Hero:
        if hero.id is not None:
            raise ValueError("Hero ID must be None")
        self.session.add(hero)
        self.session.commit()
        self.session.refresh(hero)
        return hero

    async def get_all(self, page: int = 1, page_size: int = 10) -> list[Hero]:
        result = self.session.execute(select(Hero).offset((page - 1) * page_size).limit(page_size))
        return [hero[0] for hero in result.all()]

    async def get_by_id(self, hero_id: int) -> Union[Hero, None]:
        return self.session.get(Hero, hero_id)

    async def update(self, hero: Hero) -> Hero:
        if hero.id is None:
            raise ValueError("Hero ID must be set")
        self.session.add(hero)
        self.session.commit()
        self.session.refresh(hero)
        return hero

    async def delete(self, hero_id: int) -> bool:
        hero = self.get_by_id(hero_id)
        if not hero:
            return False
        self.session.delete(hero)
        self.session.commit()
        return True
