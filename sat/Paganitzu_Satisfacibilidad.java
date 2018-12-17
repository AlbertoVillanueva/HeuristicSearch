import java.io.*;
import org.jacop.core.BooleanVar;
import org.jacop.core.Store;
import org.jacop.jasat.utils.structures.IntVec;
import org.jacop.satwrapper.SatWrapper;
import org.jacop.search.DepthFirstSearch;
import org.jacop.search.IndomainMin;
import org.jacop.search.Search;
import org.jacop.search.SelectChoicePoint;
import org.jacop.search.SimpleSelect;
import org.jacop.search.SmallestDomain;

public class Paganitzu_Satisfacibilidad {
	public static void main(String args[]) throws IOException{
		//Lectura del fichero
		FileReader fileReader = new FileReader(args[0]);
		BufferedReader bufferedReader = new BufferedReader(fileReader);
		String line;
		int filas = 0, columnas = 0;;
		int nHuecos = 0;
		Store store = new Store();
		SatWrapper satWrapper = new SatWrapper(); 
		store.impose(satWrapper);
		//Leer el fichero para determinar columnas, el numero de huecos que hay en el mapa y el numero de filas del mapa
		while((line = bufferedReader.readLine()) != null) {
			for(int columna = 0; columna < line.length();columna++){
				columnas = columna;
				if(line.charAt(columna) == ' '){
					nHuecos++;
				}
			}
			filas++;
		}
		bufferedReader.close();
		fileReader.close();
		//Volvemos a leer el fichero para determinar en que posicion estan lo huecos y se almacenan en un vector de posiciones deonde cada elemento del vector tiene la fila y columna del hueco
		fileReader = new FileReader(args[0]);
		bufferedReader = new BufferedReader(fileReader);
		posicion_t huecos[] = new posicion_t[nHuecos];
		char mapa[][] = new char [filas][columnas+1];
		nHuecos = 0;
		filas = 0;
		//Leemos el fichero y guardamos en el vector de huecos la fila y columna que le corresponde y en una matriz guardamo el mapa entero (para poder generar al final el fichero de salida)
		while((line = bufferedReader.readLine()) != null) {
			for(int columna = 0; columna < (line.length());columna++){
				if(line.charAt(columna) == ' '){
					huecos[nHuecos] = new posicion_t(filas, columna);
					nHuecos++;
				}
				mapa[filas][columna] = line.charAt(columna);
			}
			filas++;
		}
		bufferedReader.close();
		fileReader.close();
		// 1. DECLARACION DE VARIABLES
		//Varible destinada al personaje que sera un vector del tamaño del numero de huecos del mapa
		BooleanVar Al[] = new BooleanVar[nHuecos];
		for(int j = 0; j<nHuecos;j++){
			Al[j] = new BooleanVar(store, ""+j);
		}
		//Variable destinada a las serpientes que sera una matriz de tamaño numero de serpientes(argumeton) x numero de huecos
		BooleanVar Serpientes[][] = new BooleanVar[Integer.parseInt(args[1])][nHuecos];
		for(int i = 0; i<Integer.parseInt(args[1]);i++){
			for(int j = 0; j<nHuecos;j++){
				Serpientes[i][j] = new BooleanVar(store, ""+j);
			}
		}
		// Se registran las variables
		for(int i = 0; i<Integer.parseInt(args[1]);i++){
			for(int j = 0; j<nHuecos;j++){
				satWrapper.register(Serpientes[i][j]);
			}
		}
		for(int j = 0; j<nHuecos;j++){
			satWrapper.register(Al[j]);
		}

		// Todas las variables en un unico array para despues invocar al metodo que nos permite resolver el problema
		BooleanVar allVariables[] = new BooleanVar[nHuecos*(1+Integer.parseInt(args[1]))];
		int k = 0;
		for(int j = 0; j<nHuecos;j++){
			allVariables[k] = Al[j];
			k++;
		}
		for(int i = 0; i<Integer.parseInt(args[1]);i++){
			for(int j = 0; j<nHuecos;j++){
				allVariables[k] = Serpientes[i][j];
				k++;
			}
		}
		// 2. DECLARACION DE LITERALES
		int AlLiterales[] = new int[nHuecos];
		int SerpientesLiterales[][] = new int[Integer.parseInt(args[1])][nHuecos];
		for(int j = 0; j<nHuecos;j++){
			AlLiterales[j] = satWrapper.cpVarToBoolVar(Al[j], 1, true);
		}
		for(int i = 0; i<Integer.parseInt(args[1]);i++){
			for(int j = 0; j<nHuecos;j++){
				SerpientesLiterales[i][j] = satWrapper.cpVarToBoolVar(Serpientes[i][j], 1, true);
			}
		}

		// 3. RESTRICCIONES

		//1 hueco por personaje
		for(int i = 0; i<AlLiterales.length; i++){
			for(int j = 0; j<AlLiterales.length; j++){
				if(huecos[i].fila != huecos[j].fila || huecos[i].columna != huecos[j].columna){
					addClause(satWrapper, -AlLiterales[i], -AlLiterales[j]);
				}
			}
		}
		//1 hueco por serpiente
		for(int i = 0; i<SerpientesLiterales.length; i++){
			for(int j = 0; j<SerpientesLiterales[i].length; j++){
				for(int l = 0; l<SerpientesLiterales[i].length; l++){
					if(huecos[j].fila != huecos[l].fila || huecos[j].columna != huecos[l].columna){
						addClause(satWrapper, -SerpientesLiterales[i][j], -SerpientesLiterales[i][l]);
					}
				}
			}
		}
		//1 serpiente por fila
		for(int n = 0; n<SerpientesLiterales.length; n++){
			for(int j = 0; j<SerpientesLiterales[n].length; j++){
				for(int m = 0; m<SerpientesLiterales.length; m++){
					if(n!=m ){
						for(int l = 0; l<SerpientesLiterales[m].length; l++){
							if(huecos[j].fila == huecos[l].fila){
								addClause(satWrapper, -SerpientesLiterales[n][j], -SerpientesLiterales[m][l]);
							}
						}
					}
				}
			}
		}
		//columna S != columna A
		//fila S != fila A
		for (int a = 0; a < AlLiterales.length; a++) {
			for(int n = 0; n<SerpientesLiterales.length; n++){
				for(int s = 0; s<SerpientesLiterales[n].length; s++){
					//columna S != columna A
					if(huecos[s].columna == huecos[a].columna){
						addClause(satWrapper, -AlLiterales[a], -SerpientesLiterales[n][s]);
					}
					//fila S != fila A
					if(huecos[s].fila == huecos[a].fila){
						addClause(satWrapper, -AlLiterales[a], -SerpientesLiterales[n][s]);
					}
				}
			}
		}
		//hay un personaje
		addOrMultiple(satWrapper, AlLiterales);
		//hay n serpientes
		for(int n = 0; n<SerpientesLiterales.length; n++){
			addOrMultiple(satWrapper, SerpientesLiterales[n]);
		}
		// 4. INVOCAR AL SOLUCIONADOR
		
		Search<BooleanVar> search = new DepthFirstSearch<BooleanVar>();
		SelectChoicePoint<BooleanVar> select = new SimpleSelect<BooleanVar>(allVariables,new SmallestDomain<BooleanVar>(), new IndomainMin<BooleanVar>());
		Boolean result = search.labeling(store, select);
		int numHueco =0;
		String fichero = args[0] + ".output"
		FileWriter laberinto = new FileWriter (fichero);
		if (result) {
			System.out.println("Solution: ");
			for (int h = 0; h < Al.length; h++) {
				if(Al[h].value() == 1){
					System.out.println(Al[h].id());
					numHueco = Integer.parseInt(Al[h].id());
					mapa[huecos[numHueco].fila][huecos[numHueco].columna] = 'A';
				}	
			}
			for (int n = 0; n < Serpientes.length; n++) {
				for (int h = 0; h < Serpientes[n].length; h++) {
					if(Serpientes[n][h].value() == 1){
						System.out.println(Serpientes[n][h].id());
						numHueco = Integer.parseInt(Al[h].id());
						mapa[huecos[numHueco].fila][huecos[numHueco].columna] = 'S';
					}
				}
			}
			for (int i = 0; i < mapa.length; i++){
				for (int j = 0; j < mapa[i].length; j++){
					System.out.print(mapa[i][j]);
				}						
				System.out.println();
			}

			for (int i = 0; i < mapa.length; i++){
				for (int j = 0; j < mapa[i].length; j++){
					laberinto.write(mapa[i][j]);
				}						
				laberinto.write("\r\n");
			}
			laberinto.close();

		} else{
			System.out.println("*** No solution");
		}
		
		System.out.println();
	}
	//Metodo que anade una clausula del tipo x v y
	public static void addClause(SatWrapper satWrapper, int literal1, int literal2){
		IntVec clause = new IntVec(satWrapper.pool);
		clause.add(literal1);
		clause.add(literal2);
		satWrapper.addModelClause(clause.toArray());
	}
	//Método que anade clausulas del tipo (x v y v z v w ...)
	public static void addOrMultiple(SatWrapper satWrapper, int[] array){
		IntVec clause = new IntVec(satWrapper.pool);
		for(int i = 0; i<array.length;i++){
			clause.add(array[i]);
		}
		satWrapper.addModelClause(clause.toArray());
	}
}
//Clase creada para el almacenamiento de los huecos del mapa
class posicion_t{
	int fila,columna;
	public posicion_t(int fila, int columna){
		this.fila = fila;
		this.columna = columna;
	}
}
