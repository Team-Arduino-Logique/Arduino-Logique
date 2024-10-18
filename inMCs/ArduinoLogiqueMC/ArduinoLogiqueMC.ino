#include <Arduino.h>

#if defined(ESP32)
  // Code spécifique à l'ESP32
  #define LED_PIN 2

extern "C" {
  #include <malloc.h>  // Pour utiliser `mallinfo()`
}

int freeMemory() {
  struct mallinfo mi = mallinfo();
  char top;
  return &top - (char*)mi.arena;
}  
#elif defined(__AVR__)
  // Code spécifique à l'AVR (Arduino Uno)
  #include <TimerOne.h>
  #define LED_PIN 13
#else
  // Code pour d'autres plateformes
#endif



struct arg {
  byte varNum = 255;            // Variable de type byte (8 bits)
  struct arg *next = NULL;       // Pointeur vers la prochaine structure du même type (16 bits)
  byte (*func2Exec)(uint64_t pinG, uint64_t pinD, uint64_t varG, uint64_t varD) = NULL; 
};

struct arg *resFunc[128];
byte nbFunc = 0;
byte canExec = 0;
String prg = "";
uint64_t pinIOVal = 0, logicVar = 0, defPinIORW = 0, selPinIO = 0, selLogicVar = 0;

struct arg* ptrCur = NULL;
struct arg* ptrTmp = NULL;

byte setPinsFunc(uint64_t pinG, uint64_t pinD, uint64_t varG, uint64_t varD);
byte eqFunc(uint64_t pinG, uint64_t pinD, uint64_t varG, uint64_t varD);
byte andFunc(uint64_t pinG, uint64_t pinD, uint64_t varG, uint64_t varD);
byte xorFunc(uint64_t pinG, uint64_t pinD, uint64_t varG, uint64_t varD);
byte orFunc(uint64_t pinG, uint64_t pinD, uint64_t varG, uint64_t varD);
byte notFunc(uint64_t pinG, uint64_t pinD, uint64_t varG, uint64_t varD);


byte (*tblFunc[])(uint64_t pinG, uint64_t pinD, uint64_t varG, uint64_t varD) = {setPinsFunc, eqFunc, andFunc, xorFunc, orFunc, notFunc};


int serial_printf(char var, FILE *stream) {
  Serial.write(var);
  return 0;
}

// int freeMemory() {
//   extern int __heap_start, *__brkval;
//   int v;
//   return (int) &v - (__brkval == 0 ? (int) &__heap_start : (int) __brkval);
// }

void resetCode(){
    //canExec = 0;
    Serial.println("************  Reset du code *************");

    for (int i=0; i < nbFunc; i++) {
      //Serial.print("n: ");
      Serial.println(i);
      ptrTmp = resFunc[i];
      ptrCur = ptrTmp;
      while (( ptrTmp != NULL)  && (ptrTmp != resFunc[i +1])){   // ptrTmp->next->func2Exec != NULL)
          ptrCur = ptrTmp->next;
          free(ptrTmp);
          ptrTmp = ptrCur;
        }
      resFunc[i] = NULL;
    }
    nbFunc =0;   // 1e2 [ 5fa [ 5 5d9 [ 1 2 ] ] 5fa [ 6 5f2 [ 1 2 ] ] ]
}

void decodeVarNum(byte nbArgs, byte varNum, uint64_t *pinG, uint64_t *pinD, uint64_t *varG, uint64_t *varD){
    Serial.println("****************************** dans decodeVarNum *********************");
    if (nbArgs != 0) {
            if (varNum < 64) 
                  *pinD |= 1ULL << varNum;
            else  *varD |= 1ULL << (varNum -64);
            Serial.print("arg = 0 varD= ");
            Serial.println((unsigned long )*varD);
          } 
    else  {
            if (varNum < 64) 
                  *pinG |= 1ULL << varNum;
            else  *varG |= 1ULL << (varNum -64);
            Serial.print("arg > 0 varG= ");
            Serial.println((unsigned long )*varG);
          }
    Serial.println("****************************** fin decodeVarNum *********************");
}

void readPinIn(){
  for (int i = 0; i<64;i++){
    //Serial.print("(defPinIORW >> i) & 1 = ");
    //Serial.println(((defPinIORW >> i) & 1) == 0);
     if (((selPinIO >> i) & 1ULL) && (((defPinIORW >> i) & 1ULL) == 0) ) { 
       //Serial.print("dans readpin = ");
       //Serial.println(i);
        pinIOVal &= ~(1ULL << i) ;
        pinIOVal |= digitalRead(i) << i;
      }
  }
}

void code2Exec() {
  //static int32_t cpt = 0;
  //if (canExec == 1) {
    Serial.println("******************  dans code2Exec *******************");
    //String exp="";
    //String circuit="";
    //String elt="";
    //canExec = 0;
    readPinIn();
    Serial.print("début du for nbfunc : ");
    Serial.println(nbFunc);
    uint64_t selLogicVarBck = selLogicVar;
    for (int i=nbFunc; i >= 0; i--) {
      //Serial.print("n: ");
      //Serial.println(i);
      byte (*func)(uint64_t pinG, uint64_t pinD, uint64_t varG, uint64_t varD) = NULL;
      uint64_t pinD = 0, pinG = 0, varD = 0, varG = 0;
      byte firstVarNum = 255;
      byte nbArgs = 0;
      ptrTmp = resFunc[i];
      //elt="";
      //exp="";
      while ( ptrTmp != NULL) {
          Serial.print("varnum: ");
          Serial.print(ptrTmp->varNum);
          Serial.print(" -- ptrfunc: ");
          Serial.print(int(ptrTmp->func2Exec));
          Serial.print("  ptrfunc #: ");
          Serial.print(int(tblFunc[0]));
          Serial.print("  ptrfunc = : ");
          Serial.print(int(tblFunc[1]));          
          Serial.print("  ptrfunc & : ");
          Serial.println(int(tblFunc[2]));          
          //printf("func2Exec: %p  varNum: %d\n", ptrCur->func2Exec, ptrCur->varNum);
          //elt =  ( ptrTmp->func2Exec == NULL && ptrTmp->varNum == 255) ? " ]" : elt;
          //elt =  ( ptrTmp->func2Exec == 0 && ptrTmp->varNum != 255) ? " " + String(ptrTmp->varNum) : elt;
          //elt =  ( ptrTmp->func2Exec != 0 && ptrTmp->varNum == 255) ? " " + String((unsigned int)ptrTmp->func2Exec , HEX) + " [" : elt;
          //printf("%s", elt);
          //Serial.println(elt);
          //exp = exp + elt ;
          Serial.println("         ****** avant les tests *******           ");
          Serial.print("ptrTmp->func2Exec = ");
          Serial.print((int)ptrTmp->func2Exec );
          Serial.print("  ptrTmp->varNum = ");
          Serial.print((int)ptrTmp->varNum );
          Serial.print("  func = ");
          Serial.println((int)func);
          Serial.println("         ****** début des tests *******           ");
          if ( ptrTmp->func2Exec != 0){
             if (ptrTmp->varNum == 255) {
                      func = ptrTmp->func2Exec;
                      Serial.print("varNum =255 et prochaine func = ");
                      Serial.println(int(func));                      
                  }
             else decodeVarNum(nbArgs++, ptrTmp->varNum, &pinG, &pinD, &varG, &varD);
          } 
          if (ptrTmp->varNum != 255 && func !=NULL){
             Serial.print("Dans varNum = ");
             Serial.print(ptrTmp->varNum);
             Serial.print("  func = ");
             Serial.println(int(func));
             if (nbArgs == 0 ) firstVarNum = ptrTmp->varNum;
             decodeVarNum(nbArgs++, ptrTmp->varNum, &pinG, &pinD, &varG, &varD);
             Serial.println("Après decodeVarNum");
          }
          if  ( ptrTmp->func2Exec == NULL && ptrTmp->varNum == 255 && func != NULL){
              Serial.print("appel de la fonc = ");
              Serial.println(int(func));            
              byte ret = func( pinG, pinD, varG, varD);
              // si ret != 255 alors mettre dans ptrTmp->varNum = ret
              Serial.print("gestion de retour de fonc = ");
              Serial.println(ret);
              if (ret < 128) {
                          resFunc[i]->varNum = ret;
                          Serial.print("ret < 128 -> resFunc[i]->varNum : ");
                          Serial.println(i);
                      }
              else if (ret < 255) {
                         int i = 0;
                         while (( (selLogicVar >> i) && 1ULL) && (i < 64))  i++;
                         if (i < 64){
                                selLogicVar = selLogicVar  | (1ULL << i); 
                                logicVar  &= ~((ret - 128ULL) << i );
                                logicVar = logicVar | ((ret - 128ULL ) << i);
                                resFunc[i]->varNum = i + 64;
                                Serial.print("128 =< ret < 255 -> i : ");
                                Serial.println(i);
                                Serial.print("selLogicVar : ");
                                Serial.println((unsigned long)selLogicVar);
                                Serial.print("LogicVar : ");
                                Serial.println((unsigned long)logicVar);
                              }
                         else Serial.println("Limite de 64 variables atteinte!");
                      } 
              else   {
                         Serial.print("sret = 255  firstVarNum : ");
                         Serial.println(firstVarNum);
                         resFunc[i]->varNum = firstVarNum;
                     }

              // si ret = 128 0u 129 touver une varNum libre logicVar(varnum)= ret - 128 et ptrTmp->varNum = varNum libre
              Serial.println("FIN DE LA GESTION DE RET FUNC");
          }
          Serial.print("avant  ptrTmp = ptrTmp->next ptrTmp= ");
          Serial.println(int(ptrTmp));
          ptrTmp = ptrTmp->next;
        }
      //printf(" -> %s\n", exp);
      //circuit = String(exp) + circuit;    //tblFunc[0]= 0x1d4  tbl[1]= 0x408=  tbl[2]= 0x400 &   tbl[3]= 0x3e7 xor
      //circuit = circuit + String(exp) ; 
      //Serial.print(" -> ");
      // Serial.println(circuit);
    }
    //if (cpt == 1000) 
    //Serial.println(circuit);
    selLogicVar = selLogicVarBck;
  // ******************************** Revalidation de l'exécution *****************************
    // revalider l'exécution
    for (int i = 0; i <= nbFunc; i++) {
        if (resFunc[i]->func2Exec != NULL) resFunc[i]->varNum = 255;
    }
    //cpt++;
    //if (cpt> 1000) cpt =0;
  //}
  //canExec = 1;
  Serial.println("******************  FIN code2Exec *******************");
}

byte eqFunc(uint64_t pinG, uint64_t pinD, uint64_t varG, uint64_t varD) {
  byte res = 0;
  //byte gauche = 255;
  byte droite = 255;
  Serial.println("*************** dans eq func ********************");
  // Serial.print("ioval = ");
  // Serial.println((unsigned long)pinIOVal);
  // Serial.print("selPinIO = ");
  // Serial.println((unsigned long)selPinIO);
  // Serial.print("defPinIORW = ");
  // Serial.println((unsigned long)defPinIORW);

  if ( varD != 0 ) {
          //Serial.println("varD != 0");
          for (int i = 0; i < 64; i++) {
            if ((varD >> i) & 1ULL )  droite = (logicVar >> i  ) & 1ULL;
          }
        }
  else {
         // Serial.println("varD = 0");
          for (int i = 0; i < 64; i++) {
            if ((pinD >> i) & 1ULL )  droite = (pinIOVal >> i  ) & 1ULL;     
          }
          //Serial.print("droite = ");
          //Serial.println(droite);
        }
  if ( varG != 0 ) {
              //Serial.println("varG != 0");
              for (int i = 0; i < 64; i++) {
                if ((varG >> i) & 1ULL )  {
                    logicVar  &= ~(1ULL << i );
                    logicVar  |= (droite << i );
                    res =255;
                }
              }
          }
  else    {
           // Serial.println("varG = 0");
            for (int i = 0; i < 64; i++) {
                if ((pinG >> i) & 1ULL )  {
                   // Serial.print("pinIOVal avant =");
                    //Serial.println((unsigned long)pinIOVal);  
                    pinIOVal  &= ~(1ULL << i );
                    //Serial.print("pinIOVal maz =");
                    //Serial.println(~( 1 << i ));  
                    pinIOVal  |= (droite << i );
                    res =255;
                    //Serial.print("pinIOVal après =");
                    //Serial.println((unsigned long)pinIOVal);             
                }
            }
          }
  // Serial.println("********************* res eq func *******************");
  Serial.print("ioval = ");
  Serial.println((unsigned long)pinIOVal);
  Serial.print("selPinIO = ");
  Serial.println((unsigned long)selPinIO);
  Serial.print("defPinIORW = ");
  Serial.println((unsigned long)defPinIORW);
  Serial.print("logicVar = ");
  Serial.println((unsigned long)logicVar);
   Serial.println("********************* fin eq func *******************"); 

  return res;  
}

byte andFunc(uint64_t pinG, uint64_t pinD, uint64_t varG, uint64_t varD) {
  byte res = 1;
  byte i =0;
  //Serial.println("dans fonc &.");
  while ((i < 64) && (res == 1)){
      if ((varD >> i) & 1ULL )  res &= (logicVar >> i  ) & 1ULL;
      if ((varG >> i) & 1ULL )  res &= (logicVar >> i  ) & 1ULL;
      if ((pinG >> i) & 1ULL )  res &= (pinIOVal >> i  ) & 1ULL;
      if ((pinD >> i) & 1ULL )  res &= (pinIOVal >> i  ) & 1ULL;
      i++;
  }
  //Serial.print("res du & = ");
  //Serial.println(res);
  return res + 128;  
}

byte xorFunc(uint64_t pinG, uint64_t pinD, uint64_t varG, uint64_t varD) {
  byte res = 0;

  return res;  
}

byte orFunc(uint64_t pinG, uint64_t pinD, uint64_t varG, uint64_t varD) {
  byte res = 0;



  return res;  
}

byte notFunc(uint64_t pinG, uint64_t pinD, uint64_t varG, uint64_t varD) {
  byte res = 0;



  return res;  
}

byte setPinsFunc(uint64_t pinG, uint64_t pinD, uint64_t varG, uint64_t varD){
  byte res = 0;

  //Serial.println("dans set pin");
  for (int i=0; i<64; i++){
    if ((defPinIORW >> i) | 0ULL) digitalWrite(i, (pinIOVal >> i) & 1ULL);
  }
  return res;
}


byte getNumFunc(String token){
  byte numFunc;

  numFunc = 251;
  numFunc = token.equals("#") ? 0 : numFunc;
  numFunc = token.equals("=") ? 1 : numFunc;
  numFunc = token.equals("&") ? 2 : numFunc;
  numFunc = token.equals("^") ? 3 : numFunc;
  numFunc = token.equals("|") ? 4 : numFunc;
  numFunc = token.equals("~") ? 5 : numFunc;
  numFunc = token.equals("tblv") ? 6 : numFunc;
  numFunc = (token.charAt(0) == 'O') || (token.charAt(0) == 'I') || (token.charAt(0) == 'V') ? 10 : numFunc;
  numFunc = token.equals("]") ? 50 : numFunc;

  return numFunc;
}

byte compilCode(){
  byte ret = 0;
  byte numFunc = 0, pinVar = -1;
  ptrCur = NULL;
  ptrTmp = NULL;
  char delimiter = ' ';
  String token = "";

  //canExec = 0;
  nbFunc = 0;
  int endIndex = prg.indexOf(delimiter);
  Serial.print("endIndex = ");
  Serial.println(endIndex);
  //printf("tblFunc[0]= %p  tbl[1]= %p  tbl[2]= %p  tbl[3]= %p\n", tblFunc[0], tblFunc[1], tblFunc[2], tblFunc[3]);
  //int memLibre = freeMemory();
  // Serial.print("Mémoire libre : ");
  // Serial.print(memLibre);
  // Serial.println(" octets");
  while (endIndex!=-1){
      token = prg.substring(0, endIndex);
      token.trim();
      prg.remove(0, endIndex+1);
      Serial.println(token);
      //Serial.println(token);
      //Serial.print(" prg: ");
      //Serial.println(prg);
      endIndex = prg.indexOf(delimiter);
      numFunc = getNumFunc(token);
      Serial.print("numFunc = ");
      Serial.println(numFunc);
      //printf("token[0]: %c  %d\n", token.charAt(0), numFunc ); // # [ = [ O5 ^ [ I1 I2 ] ] = [ O6 & [ I1 I2 ] ] ]
      switch (numFunc) {
        case 0 :
        case 1 :
        case 2 :
        case 3 :
        case 4 :
        case 5 :
        case 6 : 
                 Serial.println("      *********   dans gestion fonction ********.       ");
                 Serial.print("nbFunc : ");
                 Serial.println(nbFunc);
                 resFunc[nbFunc] = (struct arg*) malloc(sizeof(struct arg));
                 Serial.print("dans 0..6 du switch &func : ");
                 Serial.println(String((unsigned int)tblFunc[numFunc] , HEX) ); 
                 if (resFunc[nbFunc])
                      {   
                          Serial.println("dans if") ;
                          resFunc[nbFunc]->func2Exec = tblFunc[numFunc];
                          Serial.println("après affectation") ;
                          //resFunc[n]->next = ptrCur;
                          resFunc[nbFunc]->next = NULL;
                          Serial.println("après null") ;
                          resFunc[nbFunc]->varNum = 255;
                          Serial.println("après affectation 255") ;
                          if (ptrCur != NULL) {
                              if (ptrCur->func2Exec != NULL) ptrCur->next = resFunc[nbFunc];
                          }
                          Serial.println("après ptrCur->next") ;
                          ptrCur = resFunc[nbFunc];
                          Serial.println("fin") ;
                      }
                 else Serial.println("Erreur mémoire cas 0..6");
                 nbFunc++;
                 Serial.println("      *********   FIN gestion fonction ********.       ");
                 break;
        case 10 : 
                 Serial.println("      *********   dans gestion I/O Var ********.       ");
                 ptrTmp = (struct arg*) malloc(sizeof(struct arg));
                 if (ptrTmp)
                      { 
                            ptrTmp->next = NULL; // chgt
                            if ( ptrCur->func2Exec == NULL && ptrCur->varNum == 255)
                                    resFunc[nbFunc++] = ptrTmp;
                              else  ptrCur->next = ptrTmp; // chgt
                            ptrCur = ptrTmp; // nvelle
                            pinVar = (token.substring(1)).toInt();

                            //printf("pinVar= %d\n", pinVar);
                            if (token.charAt(0) == 'V') {
                                uint64_t selVar = 1 << pinVar;
                                selLogicVar |= selVar;                      
                                pinVar += 64;
                            }
                            if (token.charAt(0) == 'I') {
                                uint64_t selPin = 1 << pinVar;
                                //defPinIORW &= !selPin ;
                                selPinIO |= selPin;
                            }
                            if (token.charAt(0) == 'O') {
                                uint64_t selPin = 1 << pinVar;
                                defPinIORW |= selPin ;
                                selPinIO |= selPin;
                            }
                            ptrCur->varNum = pinVar;
                            ptrCur->func2Exec = NULL;
                            //printf("varNum= %d\n", ptrCur->varNum );
                            Serial.print("pinVar : ");
                            Serial.println(pinVar);
                            Serial.print("selLogicVar : ");
                            Serial.println(selLogicVar);
                            Serial.print("selPinIO : ");
                            Serial.println(selPinIO);
                            Serial.print("defPinIORW : ");
                            Serial.println(defPinIORW);
                        }
                 else Serial.println("Erreur mémoire cas 10");
                 Serial.println("      *********   FIN gestion I/O Var ********.       ");
                 break;
         case 50 : ptrTmp = (struct arg*) malloc(sizeof(struct arg));
                 if (ptrTmp)
                      { 
                          ptrTmp->next = NULL; // chgt
                          if ( ptrCur->func2Exec == NULL && ptrCur->varNum == 255)
                                resFunc[nbFunc++] = ptrTmp;
                          else  ptrCur->next = ptrTmp; // chgt               ptrCur->next = ptrTmp; // chgt
                          ptrCur = ptrTmp; // nvelle
                          ptrCur->varNum = 255;
                          ptrCur->func2Exec = NULL;
                        }
                 else Serial.println("Erreur mémoire cas 50");
                 break;
      }
      //delay(10);
      Serial.print("au prochain numFunc, nbfunc = ");
      Serial.println(nbFunc);
  }
  //delay(100);
  for (int i = 0; i<64; i++){
    uint64_t selPin = 1 << i;
      Serial.print("sel pin : ");
      Serial.println(selPin);    
      if (selPinIO & selPin) {
      Serial.print("pin active : ");
      Serial.println(i);
        if (defPinIORW & selPin) 
              pinMode(i, OUTPUT);
        else  pinMode(i, INPUT);
    }
  }
  Serial.println(nbFunc);
  delay(100);
  //canExec = 1;

  //Serial.print("Mémoire libre fin de compil: ");
  //Serial.print(memLibre);
  //Serial.println(" octets");

  return ret;
}

void setup() {
  Serial.begin(9600);
    while (!Serial) {
    ; // Attente que la communication série démarre
  }
  //fdevopen(&serial_printf, NULL);
  //Timer1.initialize(50000); // 600 microsecondes
  //Timer1.attachInterrupt(code2Exec); // Attacher la fonction d'interruption
  prg = "# [ = [ O2 = [ V3 I4 ] ] ] ";
  //String prg = "# [ = [ 13 ^ [ I1 I2 ] ] = [ O6 & [ I1 I2 ] ] ]";   // # [ ^ [ I1 I45 ] ]
  //String prg = "# [ = [ O13 I4 ] = [ O6 I5 ] ] ";
  Serial.println("dans setup");
  Serial.println(prg);
  compilCode();
  canExec = 1;
  code2Exec();
  prg = "";
}

void setPinIORW(){
  Serial.println("dans setPinIORW");
  for (int i=0; i < 64; i++) {
     if (defPinIORW >> i) 
            pinMode(i, OUTPUT);
     else   pinMode(i, INPUT);
  }
}

void loop() {
    // Vérifier si des données sont disponibles sur le port série

  if (Serial.available() > 0) {
        char c = (char)Serial.read();
        prg += c;

      if (c == '\n') {
        resetCode();
        compilCode();
        Serial.println(prg);
        canExec = 1;
        prg = "";
        code2Exec();
      }
  }

  //if (canExec == 1) code2Exec();
  //delay(30000);
}
