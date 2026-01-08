package org.example.crud.entity;

import java.util.UUID;

import io.quarkus.hibernate.orm.panache.PanacheEntityBase;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "tb_users")
public class UserEntity extends PanacheEntityBase {

   @Id
   @GeneratedValue(strategy = GenerationType.UUID)
   public UUID userId;
   public String userName;

}