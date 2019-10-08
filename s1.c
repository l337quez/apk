
      // Deserilizando el JSON
      const size_t capacity = JSON_OBJECT_SIZE(1) + 10;
      DynamicJsonDocument doc(capacity);
      deserializeJson(doc, datos);
      // s1 viene como string
      String s1= doc["l1"]; //nuevo dato
      Serial.print('\n');
      Serial.println("valor de  S1");
      Serial.print(s1);


      // Actualizamos el estado de los suiches en la EEPROM

      //leemos suiche1
      EEPROM.get( eeAddress, suiche1);
      Serial.print("Valor de suiche 1:");
      Serial.println(suiche1);
      delay(3000); //esperamos a que lea

      bool rele;

      if (s1=="true")rele=HIGH;
      else rele=LOW;

      if (s1 != suiche1){  
         //Actualizamos el vaor en la EEPROM
         //Si el valor es el mismo no lo guarda.
         
//               Serial.print("valor de suiche cambio a:");
//               Serial.println(suiche1);
//
//               EEPROM.put(eeAddress, suiche1);
//               EEPROM.commit();  
//               eeAddress += sizeof(int);
//               if(eeAddress == EEPROM.length()) eeAddress = 0;
//               delay(4000);  //Espera de 4 segundos
         
          Serial.print(" DESCOMENTAR LINEAS valor de suiche grabo en la eeprom:");
          Serial.println(suiche1);
         
         digitalWrite(16, rele); 

         
      } // FIN if (s1 != suiche1)

//suiche1=HIGH;
//  EEPROM.put( eeAddress, suiche1 );  //Grabamos el valor
//  eeAddress += sizeof(float);  //Obtener la siguiente posicion para escribir
//  if(eeAddress >= EEPROM.length()) eeAddress = 0;  //Comprobar que no hay desbordamiento
//  EEPROM.commit();
//  delay(30000); //espera 30 segunos



////if (s1 != suiche1){ //nunca va pasar que sean iguales
////  
    //Actualizamos el vaor en la EEPROM
    //Si el valor es el mismo no lo guarda.
     suiche1=s1;
Serial.print("valor de suiche cambio a:");
Serial.println(suiche1);
////
////     
////     EEPROM.put(eeAddress, suiche1);
////     EEPROM.commit();  
////     eeAddress += sizeof(int);
////     if(eeAddress == EEPROM.length()) eeAddress = 0;
////     delay(4000);  //Espera de 4 segundos
////Serial.print("valor de suiche grabo en la eeprom:");
////Serial.println(suiche1);
////     
////     digitalWrite(16, suiche1);  

        
         Serial.print("limpiamos datos");
         //Limpiamos 
         str_len=0;
         //limpiamos  la concatenacion
         datos="";

