package org.example.crud.service;

import java.util.List;
import java.util.UUID;

import org.example.crud.entity.UserEntity;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.ws.rs.WebApplicationException;

@ApplicationScoped
public class UserService {

    public UserEntity createUser(UserEntity userEntity) {
        UserEntity.persist(userEntity);
        return userEntity;
    }

    public UserEntity updateUser(UUID id, UserEntity userEntity) {
        UserEntity existingUser = (UserEntity) UserEntity.findByIdOptional(id).orElseThrow(() -> new WebApplicationException("User not found", 404));
        existingUser.userName = userEntity.userName;
        UserEntity.persist(existingUser);
        return existingUser;
    }

    public List<UserEntity> findAll(int page, int pageSize) {
        return UserEntity.findAll()
                .page(page, pageSize)
                .list();
    }

    public UserEntity findById(UUID id) {

        return (UserEntity) UserEntity.findByIdOptional(id).orElseThrow(() -> new WebApplicationException("User not found", 404));

    }

    public void deleteUser(UUID id) {
        UserEntity userEntity = (UserEntity) UserEntity.findByIdOptional(id).orElseThrow(() -> new WebApplicationException("User not found", 404));
        UserEntity.delete("userId", userEntity.userId);
    }

}
