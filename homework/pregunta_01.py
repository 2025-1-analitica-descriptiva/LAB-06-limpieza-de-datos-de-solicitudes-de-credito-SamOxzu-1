"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""
import pandas as pd
import os


def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """

    def load_data(input_file):
        """Lea el archivo usando pandas y devuelva un DataFrame"""
        df = pd.read_csv(input_file, delimiter=';', index_col=0)
        return df

    def clean_data(df):
        """Limpia los datos eliminando duplicados y manejando datos faltantes."""
        df = df.copy()

        # Eliminar duplicados
        df = df.drop_duplicates()

        # Eliminar
        df = df.dropna()
        
        # Convertir fechas
        df["year"] = df["fecha_de_beneficio"].map(
            lambda x: (
                int(x.split("/")[0])
                if len(x.split("/")[0]) > 2
                else int(x.split("/")[-1])
            )
        )
        df["month"] = df["fecha_de_beneficio"].map(lambda x: int(x.split("/")[1]))
        df["day"] = df["fecha_de_beneficio"].map(
            lambda x: (
                int(x.split("/")[-1])
                if len(x.split("/")[0]) > 2
                else int(x.split("/")[0])
            )
        )
        df["fecha_de_beneficio"] = pd.to_datetime(df[["year", "month", "day"]])

        df = df.drop(columns=["year", "month", "day"])


        # Limpieza de cadenas de texto
        columns = df.columns.tolist()
        columns.remove("barrio")

        df["barrio"] = df["barrio"].map(
            lambda x: x.lower().replace("_", "-").replace("-", " ")
        )

        df[columns] = df[columns].map(
            lambda x: (
                x.lower()
                .replace("-", " ")
                .replace("_", " ")
                .replace("$", "")
                .replace(".00", "")
                .replace(",", "")
                .strip()
                if isinstance(x, str)
                else x
            )
        )

        # Eliminar registros duplicados nuevamente
        df = df.drop_duplicates()
        return df


    def save_data(df, output_dir):
        """Guarda el DataFrame en un archivo CSV."""
        # Crear el directorio si no existe
        output_dir = os.path.dirname(output_dir)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Guardar el archivo CSV en la ruta especificada
        df.to_csv(os.path.join(output_dir, "solicitudes_de_credito.csv"), sep=";", index=False)

    def main(input_file, output_dir):
        """Ejecuta la limpieza de datos."""
        df = load_data(input_file)
        df = clean_data(df)
        save_data(df, output_dir)

    if __name__ == "__main__":
        main(
            input_file="files/input/solicitudes_de_credito.csv",
            output_dir="files/output/" 
        )

print(pregunta_01())