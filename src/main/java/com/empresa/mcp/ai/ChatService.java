
package com.empresa.mcp.ai;

import dev.langchain4j.model.anthropic.AnthropicChatModel;
import dev.langchain4j.service.AiServices;
import jakarta.enterprise.context.ApplicationScoped;

import com.empresa.mcp.mcp.tools.CandidateTool;

@ApplicationScoped   
public class ChatService {

    interface RecruiterAssistant {
        String chat(String message);
    }

    private final RecruiterAssistant assistant;

    public ChatService() {
        var model = AnthropicChatModel.builder()
            .apiKey(System.getenv("ANTHROPIC_API_KEY"))
            .modelName("claude-3-7-sonnet")
            .build();

        this.assistant = AiServices.builder(RecruiterAssistant.class)
            .chatLanguageModel(model)
            .tools(new CandidateTool())
            .build();
    }

    public String ask(String message) {
        return assistant.chat(message);
    }
}
