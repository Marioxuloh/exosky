using UnityEngine;

public class ExoplanetInfoDisplay : MonoBehaviour
{
    public GameObject planet; // Referencia a la esfera del planeta

    private void Start()
    {
        Debug.Log("Asignando material a la esfera...");

        // Verificar que hay al menos un exoplaneta en la lista
        if (GlobalData.Exoplanets.Count > 0)
        {
            Exoplanet exoplanet = GlobalData.Exoplanets[0]; // Obtener el único exoplaneta

            // Asignar el material correspondiente a la esfera (instanciar el material)
            if (planet.GetComponent<Renderer>() != null)
            {
                planet.GetComponent<Renderer>().material = new Material(exoplanet.material); // Asigna el material directamente
                Debug.Log("Asignado material " + exoplanet.material + " al exoplaneta: " + exoplanet.pl_name);
            }
        }
        else
        {
            Debug.LogError("No hay exoplanetas en la lista de GlobalData.");
        }
    }
}
