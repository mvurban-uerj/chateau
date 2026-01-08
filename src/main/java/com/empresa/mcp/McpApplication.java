package com.empresa.mcp;

import io.quarkus.runtime.Quarkus;
import io.quarkus.runtime.annotations.QuarkusMain;

@QuarkusMain
public class McpApplication {

    public static void main(String[] args) {
        Quarkus.run(args);
    }
}
