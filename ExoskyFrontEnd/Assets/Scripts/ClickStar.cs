using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Networking;
using System.Text;
using System;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Threading.Tasks;

[System.Serializable]
public class Constellar
{
    public List<ConstellarGuide> constellarsGuide = new List<ConstellarGuide>();
}

[System.Serializable]
public class ConstellarGuide
{
    public string starA;
    public string starB;
    public GameObject line;
    public bool isCreated;

    public ConstellarGuide(string starA, string starB)
    {
        this.starA = starA;
        this.starB = starB;
        this.line = null; // Inicializar en null
        this.isCreated = false;
    }
}

[System.Serializable]
public class SaveData
{
    public string user_name = PlayerPrefs.GetString("Username", "Guest");
    public string pl_name = GlobalData.Exoplanets[0].pl_name;
    public List<string> coordenates = new List<string>(); // Cambiado a List<string>
}

[System.Serializable]
public class ConstellarDataArray
{
    public ConstellarDataFromJson[] result;
}

[System.Serializable]
public class ConstellarDataFromJson
{
    public int id;
    public string exoplanet;
    public string user;
    public string[] coordenates;
}

public class GetExoplanet
{
    public string pl_name;
}

public class ClickStar : MonoBehaviour
{
    private string url = "http://127.0.0.1:8000/constellations/constellationinsert/";
    private string urlConstellations = "http://127.0.0.1:8000/constellations/constellationsbyexoplanet/";
    public float maxDistance = 500f;
    public List<Constellar> constellars = new List<Constellar>();
    public bool createMode;
    public GameObject panelCreate;
    public GameObject panelSave;

    private GameObject selectedStarA;
    private GameObject selectedStarB;
    private Color originalColorA;
    private Color originalColorB;
    private HttpClient client; // Cambiado a variable de instancia

    void Start()
    {
        client = new HttpClient();
        client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
        CreateInitialConstellar();
    }

    void Update()
    {
        if (Input.GetMouseButtonDown(0) && createMode)
        {
            this.SelectStars();
        }

        if(PlayerPrefs.GetString("onLoadStars", "") == "true")
        {
            Debug.Log("Buscando constelaciones...");
            StartCoroutine(GetConstelars());
            PlayerPrefs.SetString("onLoadStars", "false");
        }
    }

    private void SelectStars()
    {
        Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);
        if (Physics.Raycast(ray, out RaycastHit hit, maxDistance))
        {
            GameObject selectedObject = hit.transform.gameObject;
            Renderer renderer = selectedObject.GetComponent<Renderer>();

            if (selectedStarA == null)
            {
                // Selección de la primera estrella
                selectedStarA = selectedObject;
                originalColorA = renderer.material.color;
                renderer.material.color = Color.blue;
            }
            else if (selectedStarB == null && selectedObject != selectedStarA)
            {
                // Selección de la segunda estrella
                selectedStarB = selectedObject;
                originalColorB = renderer.material.color;
                renderer.material.color = Color.blue;

                // Agregar las estrellas a la última constelación
                if (constellars.Count > 0)
                {
                    constellars[constellars.Count - 1].constellarsGuide.Add(new ConstellarGuide(selectedStarA.name, selectedStarB.name));
                    CreateConnections();
                }

                ResetStarColors();
            }
        }
    }

    private void ResetStarColors()
    {
        if (selectedStarA != null && selectedStarB != null)
        {
            selectedStarA.GetComponent<Renderer>().material.color = originalColorA;
            selectedStarB.GetComponent<Renderer>().material.color = originalColorB;
            selectedStarA = null;
            selectedStarB = null;
        }
    }

    public void CreateConnections()
    {
        var lastConstellar = constellars[constellars.Count - 1]; // Obtener la última constelación
        foreach (ConstellarGuide guide in lastConstellar.constellarsGuide)
        {
            if (!guide.isCreated)
            {
                GameObject starA = GameObject.Find(guide.starA);
                GameObject starB = GameObject.Find(guide.starB);

                if (starA != null && starB != null)
                {
                    GameObject line = GameObject.CreatePrimitive(PrimitiveType.Cylinder);
                    Vector3 midpoint = (starA.transform.position + starB.transform.position) / 2;
                    line.transform.position = midpoint;
                    Vector3 direction = starB.transform.position - starA.transform.position;
                    float distance = direction.magnitude;
                    line.transform.localScale = new Vector3(0.1f, distance / 2, 0.1f);
                    line.transform.up = direction.normalized;

                    guide.line = line; // Asignar línea
                    guide.isCreated = true; // Marcar como creada
                }
            }
        }
    }

    public void SetCreateConstellar()
    {
        // Crear un nuevo constellar al iniciar el modo de creación
        Constellar newConstellar = new Constellar(); // Crear sin nombre
        constellars.Add(newConstellar); // Agregar a la lista

        createMode = true;
        panelCreate.SetActive(false);
        panelSave.SetActive(true);
    }

    public void SaveConstelars()
    {
        // Enviar el JSON a la API
        SendConstellarData();

        createMode = false;
        panelCreate.SetActive(true);
        panelSave.SetActive(false);
    }

    private async void SendConstellarData()
    {
        // Solo obtener la última constelación creada
        var lastConstellar = constellars[constellars.Count - 1];

        // Crear el JSON para enviar
        var saveData = new SaveData
        {
            coordenates = new List<string>()
        };

        // Agregar las coordenadas como pares
        foreach (var guide in lastConstellar.constellarsGuide)
        {
            saveData.coordenates.Add($"{guide.starA}, {guide.starB}");
        }

        string jsonData = JsonUtility.ToJson(saveData);

        Debug.Log(jsonData);

        // Create a new request to send the JSON to the backend
        using (var client = new HttpClient())
        {
            // Configurar el cliente
            client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));

            // Crear el contenido de la solicitud
            var content = new StringContent(jsonData, Encoding.UTF8, "application/json");

            Debug.Log(content);

            try
            {
                // Enviar la solicitud POST
                var response = await client.PostAsync(url, content); // Reemplaza con tu URL de API

                // Asegurarse de que la respuesta fue exitosa
                response.EnsureSuccessStatusCode();

                // Leer el contenido de la respuesta
                var responseBody = await response.Content.ReadAsStringAsync();
                Debug.Log("Respuesta de la API: " + responseBody);
            }
            catch (HttpRequestException e)
            {
                Debug.Log("Error en la solicitud: " + e.Message);
            }
        }
    }

    public void CancelCreateConstelar()
    {
        createMode = false;
        RemoveEmptyConstellarGuides();
        panelCreate.SetActive(true);
        panelSave.SetActive(false);
    }

    public void RemoveEmptyConstellarGuides()
    {
        constellars.RemoveAll(constellar => constellar.constellarsGuide.Count == 0);
    }

    private void CreateInitialConstellar()
    {
        constellars.Add(new Constellar()); // Crear una constelación inicial
    }

    private IEnumerator GetConstelars()
    {
        Exoplanet exoplanet = GlobalData.Exoplanets[0];

        // Crear el contenido de la solicitud
        var jsonData = JsonUtility.ToJson(new GetExoplanet{
            pl_name = exoplanet.pl_name
        });

        Debug.Log(jsonData);

        // Create a new request to send the JSON to the backend
        using (UnityWebRequest www = UnityWebRequest.Post(urlConstellations, jsonData, "application/json"))
        {
            yield return www.SendWebRequest();

            try
            {
                // Leer el contenido de la respuesta
                var responseBody = www.downloadHandler.text;

                this.CreateOldConnections(responseBody);
            }
            catch (HttpRequestException e)
            {
                Debug.Log("Error en la solicitud: " + e.Message);
            }
        }
    }

    public void CreateOldConnections(string oldConstellars)
    {
        Debug.Log(oldConstellars.GetType());
        // Deserializar el JSON
        var constellarsData = JsonUtility.FromJson<ConstellarDataArray>(oldConstellars);
        Debug.Log(constellarsData);

        // Crear un nuevo Constellar
        Constellar newConstellar = new Constellar();

        foreach(var constellarData in constellarsData.result)
        {
            // Llenar la lista de ConstellarGuide con las coordenadas
            foreach (var coordinate in constellarData.coordenates)
            {
                // Separar las estrellas por ", "
                string[] stars = coordinate.Split(new string[] { ", " }, StringSplitOptions.None);
                if (stars.Length == 2)
                {
                    ConstellarGuide guide = new ConstellarGuide(stars[0], stars[1]);
                    newConstellar.constellarsGuide.Add(guide);
                }
            }
        }

        foreach (ConstellarGuide guide in newConstellar.constellarsGuide)
        {
            if (!guide.isCreated)
            {
                GameObject starA = GameObject.Find(guide.starA);
                GameObject starB = GameObject.Find(guide.starB);

                if (starA != null && starB != null)
                {
                    GameObject line = GameObject.CreatePrimitive(PrimitiveType.Cylinder);
                    Vector3 midpoint = (starA.transform.position + starB.transform.position) / 2;
                    line.transform.position = midpoint;
                    Vector3 direction = starB.transform.position - starA.transform.position;
                    float distance = direction.magnitude;
                    line.transform.localScale = new Vector3(0.1f, distance / 2, 0.1f);
                    line.transform.up = direction.normalized;

                    guide.line = line; // Asignar línea
                    guide.isCreated = true; // Marcar como creada
                }
            }
        }
    }
}
