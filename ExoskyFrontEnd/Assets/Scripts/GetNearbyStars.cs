using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Networking;
using System.Text;
using System;

[System.Serializable]
public class CloudNearby
{
    public double ra;
    public double dec;
    public double parsecs;
    public double visible_distance;
    public double n_stars;
    public double phot_g_mean_mag;
}

// Clase para representar los datos de XYZ
[System.Serializable]
public class StarPosition
{
    public string[] dist_central;
    public string[] DESIGNATION;
    public string[] ra;
    public string[] dec;
    public string[] distance_gspphot;
    public string[] parallax;
    public string[] bp_rp;
    public string[] X;
    public string[] Y;
    public string[] Z;
    public float[] X_sphere;
    public float[] Y_sphere;
    public float[] Z_sphere;
    public float[] radius_sphere;
    public float[] color_r;
    public float[] color_g;
    public float[] color_b;
}

public class GetNearbyStars : MonoBehaviour
{
    // Referencia al objeto "CenterStars" en la escena
    public Transform centerStars;
    public StarPosition starPositions;
    public GameObject planet;
    public GameObject panelLoading;

    private string apiUrl = "http://127.0.0.1:8000/gaia/nearbystars/"; // Reemplaza con tu URL del backend

    // Start is called before the first frame update
    void Start()
    {
        Debug.Log("Llamando al API");
        StartCoroutine(GetStarsCloud());
    }

    // Update is called once per frame
    void Update()
    {
    }

    private IEnumerator GetStarsCloud()
    {
        Exoplanet exoplanet = GlobalData.Exoplanets[0];
        planet.GetComponent<Renderer>().material = new Material(exoplanet.material);

        // Crear los datos JSON para enviar
        string jsonData = JsonUtility.ToJson(new CloudNearby
        {
            ra = exoplanet.ra,
            dec = exoplanet.dec,
            parsecs = exoplanet.sy_dist,
            visible_distance = 100,
            n_stars = 10000
        });

        // Crear el request usando UnityWebRequest
        UnityWebRequest request = new UnityWebRequest(apiUrl, "POST");
        
        byte[] bodyRaw = Encoding.UTF8.GetBytes(jsonData);
        request.uploadHandler = new UploadHandlerRaw(bodyRaw);
        request.downloadHandler = new DownloadHandlerBuffer();
        request.SetRequestHeader("Content-Type", "application/json");

        // Enviar la solicitud y esperar la respuesta
        yield return request.SendWebRequest();

        // Comprobar si hay errores en la solicitud
        if (request.result != UnityWebRequest.Result.Success)
        {
            Debug.Log("Error en la solicitud: " + request.error);
        }
        else
        {
            // Leer la respuesta
            string responseBody = request.downloadHandler.text;
            Debug.Log("Respuesta de la API: " + responseBody);

            // Parsear el array de posiciones desde el JSON de la respuesta
            this.starPositions = JsonUtility.FromJson<StarPosition>(responseBody);

            int numStars = this.starPositions.X_sphere.Length;

            Debug.Log("numStars: " + numStars);

            // Crear esferas en las posiciones XYZ
            for (int i = 0; i < numStars; i++)
            {
                Vector3 position = new Vector3(this.starPositions.X_sphere[i], this.starPositions.Y_sphere[i], this.starPositions.Z_sphere[i]);

                GameObject sphere = GameObject.CreatePrimitive(PrimitiveType.Sphere);

                // Asignar el nombre usando DESIGNATION
                sphere.name = this.starPositions.DESIGNATION[i];

                // Crear una esfera en la posición especificada
                sphere.transform.position = position;

                // Ajustar la escala de la esfera usando radius_sphere
                float radius = this.starPositions.radius_sphere[i];
                sphere.transform.localScale = new Vector3(radius, radius, radius);

                // Cambiar el color de la esfera usando los valores de color_r, color_g, color_b
                Material material = new Material(Shader.Find("Custom/SimpleShader"));
                material.color = new Color(this.starPositions.color_r[i], this.starPositions.color_g[i], this.starPositions.color_b[i]);
                // Asignar el material al renderer de la esfera
                Renderer sphereRenderer = sphere.GetComponent<Renderer>();
                sphereRenderer.material = material;
                // Hacer de "CenterStars" el padre de la esfera
                sphere.transform.parent = centerStars;
            }

            PlayerPrefs.SetString("onLoadStars", "true");
            this.panelLoading.SetActive(false);
        }
    }
}
