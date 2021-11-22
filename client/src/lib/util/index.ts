export function parseFastAPIError(e: Record<string, unknown>): string {
  const { message, detail } = e;
  if (typeof detail === "string") return detail;
  if (typeof message === "string") return message;
  if (Array.isArray(detail))
    return detail
      .filter((d, i) => i + 1 + ". " + (d.msg || "An unknown error occured"))
      .join("\n");
  return "An unknown error occured";
}
