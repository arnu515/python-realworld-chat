/*
  Warnings:

  - You are about to drop the column `providerData` on the `User` table. All the data in the column will be lost.
  - You are about to drop the column `providerId` on the `User` table. All the data in the column will be lost.

*/
-- AlterTable
ALTER TABLE "User" DROP COLUMN "providerData",
DROP COLUMN "providerId",
ADD COLUMN     "provider_data" JSON,
ADD COLUMN     "provider_id" VARCHAR(255);
