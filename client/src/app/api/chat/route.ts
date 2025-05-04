import { openai } from "@ai-sdk/openai";
import { streamText, generateText } from "ai";

export async function POST(req: Request) {
    const { messages } = await req.json();
    const result = streamText({
        model: openai.chat("gpt-4.1-nano"),
        messages,
    });
    return result.toDataStreamResponse();
}
