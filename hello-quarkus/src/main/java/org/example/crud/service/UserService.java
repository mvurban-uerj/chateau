package org.example.crud.service;
import org.example.crud.entity.UserEntity;
import jakarta.enterprise.context.ApplicationScoped;
import java.util.List;

@ApplicationScoped
public class UserService {
 
   public UserEntity createUser(UserEntity userEntity){

      UserEntity.persist(userEntity);
      return userEntity;

   }

   public List<UserEntity> findAll(int page, int pageSize) {
      return UserEntity.findAll()
            .page(page, pageSize)
            .list();
   }

}
