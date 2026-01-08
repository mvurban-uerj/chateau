package org.example.crud.controller;

import java.util.List;
import java.util.UUID;

import org.example.crud.entity.UserEntity;
import org.example.crud.service.UserService;

import jakarta.transaction.Transactional;
import jakarta.ws.rs.Consumes;
import jakarta.ws.rs.DELETE;
import jakarta.ws.rs.DefaultValue;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.POST;
import jakarta.ws.rs.PUT;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.PathParam;
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

   //CREATE USER   
   @POST
   @Transactional
   public Response createUser(UserEntity userEntity) {      
      return Response.ok(userService.createUser(userEntity)).build();
   }

   //Update User
   @PUT
   @Path("/{id}")
   @Transactional
   public Response updateUser(@PathParam("id") UUID id, UserEntity userEntity) {      
      return Response.ok(userService.updateUser(id, userEntity)).build();
   }  


   //FIND ALL WITH PAGINATION
   @GET
   public Response findAll(@QueryParam("page") @DefaultValue("0") int page,
                           @QueryParam("pageSize") @DefaultValue("10") int pageSize ) {      
       List<UserEntity> users = userService.findAll(page, pageSize);
       return Response.ok(users).build();
   }

   //FIND BY ID
   @GET
   @Path("/{id}")
   public Response findById(@PathParam("id") UUID id) {      
      UserEntity user = userService.findById(id);
      return Response.ok(user).build();
   }

   //DELETE USER 
   @DELETE
   @Path("/{id}")
   @Transactional
   public Response deleteUser(@PathParam("id") UUID id) {      
      
      userService.deleteUser(id);
      return Response.noContent().build();
      
   }






}
