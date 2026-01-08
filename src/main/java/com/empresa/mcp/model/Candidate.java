
package com.empresa.mcp.model;

public record Candidate(
    String name,
    String[] skills,
    String[] languages,
    double score
) {}
