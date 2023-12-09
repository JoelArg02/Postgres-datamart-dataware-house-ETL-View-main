// init-mongo.js
db.createCollection("usuarios", {
    validator: {
       $jsonSchema: {
          bsonType: "object",
          required: ["nombre_usuario", "correo"],
          properties: {
             nombre_usuario: { bsonType: "string" },
             correo: { bsonType: "string" },
             amigos: { bsonType: "array" }
          }
       }
    }
 });
 
 db.createCollection("publicaciones", {
    validator: {
       $jsonSchema: {
          bsonType: "object",
          required: ["id_usuario", "contenido", "fecha_publicacion"],
          properties: {
             id_usuario: { bsonType: "objectId" },
             contenido: { bsonType: "string" },
             fecha_publicacion: { bsonType: "date" },
             likes: { bsonType: "array" }
          }
       }
    }
 });
 
 db.createCollection("comentarios", {
    validator: {
       $jsonSchema: {
          bsonType: "object",
          required: ["id_publicacion", "id_usuario", "texto", "fecha_comentario"],
          properties: {
             id_publicacion: { bsonType: "objectId" },
             id_usuario: { bsonType: "objectId" },
             texto: { bsonType: "string" },
             fecha_comentario: { bsonType: "date" }
          }
       }
    }
 });
 