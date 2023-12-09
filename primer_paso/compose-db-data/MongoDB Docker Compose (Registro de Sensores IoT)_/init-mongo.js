// init-mongo.js
db.createCollection("dispositivos", {
    validator: {
       $jsonSchema: {
          bsonType: "object",
          required: ["nombre_dispositivo", "tipo", "ubicacion"],
          properties: {
             nombre_dispositivo: { bsonType: "string" },
             tipo: { bsonType: "string" },
             ubicacion: { bsonType: "string" }
          }
       }
    }
 });
 
 db.createCollection("lecturas_sensores", {
    validator: {
       $jsonSchema: {
          bsonType: "object",
          required: ["id_dispositivo", "tipo_sensor", "valor", "fecha_lectura"],
          properties: {
             id_dispositivo: { bsonType: "objectId" },
             tipo_sensor: { bsonType: "string" },
             valor: { bsonType: "double" },
             fecha_lectura: { bsonType: "date" }
          }
       }
    }
 });
 
 db.createCollection("alertas", {
    validator: {
       $jsonSchema: {
          bsonType: "object",
          required: ["id_dispositivo", "tipo_alerta", "fecha_alerta", "estado"],
          properties: {
             id_dispositivo: { bsonType: "objectId" },
             tipo_alerta: { bsonType: "string" },
             fecha_alerta: { bsonType: "date" },
             estado: { bsonType: "string" }
          }
       }
    }
 });
 