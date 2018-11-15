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
		FileReader fileReader = new FileReader(args[0]);
		BufferedReader bufferedReader = new BufferedReader(fileReader);
		String line;
		int filas = 0, columnas;
		int nHuecos = 0;
		Store store = new Store();
		SatWrapper satWrapper = new SatWrapper(); 
		store.impose(satWrapper);

		while((line = bufferedReader.readLine()) != null) {
			for(int columna = 0; columna < line.length();columna++){
				if(line.charAt(columna) == ' '){
					nHuecos++;
				}
			}
		}
		bufferedReader.close();
		fileReader.close();
		fileReader = new FileReader(args[0]);
		bufferedReader = new BufferedReader(fileReader);
		posicion_t huecos[] = new posicion_t[nHuecos];
		nHuecos = 0;
		while((line = bufferedReader.readLine()) != null) {
			for(int columna = 0; columna < line.length();columna++){
				if(line.charAt(columna) == ' '){
					huecos[nHuecos] = new posicion_t(filas, columna);
					nHuecos++;
				}
			}
			filas++;
		}
		bufferedReader.close();
		fileReader.close();
		// 1. DECLARACION DE VARIABLES
		BooleanVar Al[] = new BooleanVar[nHuecos];
		for(int j = 0; j<nHuecos;j++){
			Al[j] = new BooleanVar(store, "\n Al esta en hueco "+j);
		}
		BooleanVar Serpientes[][] = new BooleanVar[Integer.parseInt(args[1])][nHuecos];
		for(int i = 0; i<Integer.parseInt(args[1]);i++){
			for(int j = 0; j<nHuecos;j++){
				Serpientes[i][j] = new BooleanVar(store, "\n Serpiente "+i+" esta en hueco "+j);
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
		int SerpientesLiterales[][] = new int[Integer.parseInt(args[1]][nHuecos];
		for(int j = 0; j<nHuecos;j++){
			AlLiterales[j] = satWrapper.cpVarToBoolVar(Al[j], 1, true);
		}
		for(int i = 0; i<Integer.parseInt(args[1]);i++){
			for(int j = 0; j<nHuecos;j++){
				int SerpientesLiterales[i][j] = satWrapper.cpVarToBoolVar(Serpientes[i][j], 1, true);
			}
		}

		// 3. RESTRICCIONES
	}
	public static void addClause(SatWrapper satWrapper, int literal1, int literal2){

	}
	public static void implicacionMultiple(int implicador, int[] implicados){

	}
}
class posicion_t{
	int fila,columna;
	public posicion_t(int fila, int columna){
		this.fila = fila;
		this.columna = columna;
	}
}
