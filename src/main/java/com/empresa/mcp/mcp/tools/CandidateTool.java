
package com.empresa.mcp.mcp.tools;

import dev.langchain4j.agent.tool.Tool;
import jakarta.enterprise.context.ApplicationScoped;

import com.empresa.mcp.model.Candidate;
import java.util.List;

@ApplicationScoped
public class CandidateTool {

   /**
    * Busca candidatos com base em requisitos profissionais
    * como linguagem de programação, idiomas e área de atuação.
    *
    * @param query descrição textual do perfil desejado
    * @return lista de candidatos compatíveis
    */
   @Tool
   public List<Candidate> findCandidates(String requirements) {
      return List.of(
            new Candidate(
                  "Maria Silva",
                  new String[] { "Java", "Spring", "Políticas Públicas" },
                  new String[] { "Português", "Inglês" },
                  0.89),
             new Candidate(
                "Maria Souza",
                new String[] { "Java Avançado", "Spring adv", "Governo Digital" },
                new String[] { "Inglês fluente" },
                0.85)
            );
   }
}
