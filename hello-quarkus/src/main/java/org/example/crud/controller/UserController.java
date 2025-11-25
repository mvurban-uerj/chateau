package org.example.crud.controller;

import java.util.List;

import org.example.crud.entity.UserEntity;
import org.example.crud.service.UserService;

import jakarta.transaction.Transactional;
import jakarta.ws.rs.Consumes;
import jakarta.ws.rs.DefaultValue;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.POST;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.QueryParam;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;

@Path("/users")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class UserController {
   
   private final UserService userService;

   public UserController(UserService userService) {
      this.userService = userService;
   }


   @GET
   public Response findAll(@QueryParam("page") @DefaultValue("0") int page,
                           @QueryParam("pageSize") @DefaultValue("10") int pageSize ) {      
       List<UserEntity> users = userService.findAll(page, pageSize);
       return Response.ok(users).build();
   }

   @POST
   @Transactional
   public Response createUser(UserEntity userEntity) {      
      return Response.ok(userService.createUser(userEntity)).build();
   }

}
