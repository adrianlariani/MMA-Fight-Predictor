"use server";

import { stat } from "fs";
import prisma from "./prisma";
import { fighter_statistics } from "@prisma/client";

export async function getAllFighters() {
  try {
    const statistics = await prisma.fighter_statistics.findMany({ take: 100 });
    console.log(statistics);
    return await prisma.fighter_statistics.findMany();
  } catch (error) {
    console.error("Database Error:", error);
    throw new Error("Failed to get all fighters" + error);
  }
}

export async function getFightersByText(text: string) {
  try {
    return await prisma.fighter_statistics.findMany({
      take: 100,
      where: { name: { contains: text, mode: "insensitive" } },
    });
  } catch (error) {
    console.error("Database Error:", error);
    throw new Error("Failed to get fighter by text" + error);
  }
}

export async function getFighterByID(id: number) {
  try {
    return await prisma.fighter_statistics.findFirst({ where: { id: id } });
  } catch (error) {
    console.error("Database Error:", error);
    throw new Error("Failed to get fighter by ID" + error);
  }
}

export async function getFighterImageByID(id: number) {
  try {
    const fighter = await prisma.fighter_statistics.findFirst({
      where: { id: id },
    });
    return fighter?.image_link;
  } catch (error) {
    console.error("Database Error:", error);
    throw new Error("Failed to get fighter image by ID" + error);
  }
}

export async function mapFightersNames(input: string) {
  const fighters = await getFightersByText(input);

  return await fighters.map((fighter) => ({
    label: fighter.name,
    value: fighter.id,
  }));
}
