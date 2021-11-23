/*
  Warnings:

  - A unique constraint covering the columns `[from_user_id]` on the table `ChatRequest` will be added. If there are existing duplicate values, this will fail.
  - A unique constraint covering the columns `[to_user_id]` on the table `ChatRequest` will be added. If there are existing duplicate values, this will fail.

*/
-- CreateIndex
CREATE UNIQUE INDEX "ChatRequest_from_user_id_key" ON "ChatRequest"("from_user_id");

-- CreateIndex
CREATE UNIQUE INDEX "ChatRequest_to_user_id_key" ON "ChatRequest"("to_user_id");
