package com.empresa.mcp.api;
import com.empresa.mcp.ai.ChatService;
import jakarta.inject.Inject;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.MediaType;

@Path("/chat")
@Consumes(MediaType.TEXT_PLAIN)
@Produces(MediaType.TEXT_PLAIN)
public class ChatResource {
   @Inject
    ChatService chatService;

    @POST
    public String chat(String message) {
        return chatService.ask(message);
    }
}

// package com.empresa.mcp.api;

// import jakarta.ws.rs.POST;
// import jakarta.ws.rs.Path;
// import jakarta.ws.rs.Consumes;
// import jakarta.ws.rs.Produces;
// import jakarta.ws.rs.core.MediaType;
// import jakarta.ws.rs.core.Response;

// @Path("/chat")
// public class ChatResource {

//     @POST
//     @Consumes(MediaType.TEXT_PLAIN)
//     @Produces(MediaType.TEXT_PLAIN)
//     public Response chat(String message) {
//         System.out.println("Recebi: " + message);
//         return Response.ok("OK: " + message).build();
//     }
// }
