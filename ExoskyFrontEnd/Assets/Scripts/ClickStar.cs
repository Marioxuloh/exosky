using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Networking;
using System.Text;
using System;

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

    void Start()
    {
        CreateInitialConstellar();
    }

    void Update()
    {
        if (Input.GetMouseButtonDown(0) && createMode)
        {
            this.SelectStars();
        }

        if (PlayerPrefs.GetString("onLoadStars", "") == "true")
        {
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
                selectedStarA = selectedObject;
                originalColorA = renderer.material.color;
                renderer.material.color = Color.blue;
            }
            else if (selectedStarB == null && selectedObject != selectedStarA)
            {
                selectedStarB = selectedObject;
                originalColorB = renderer.material.color;
                renderer.material.color = Color.blue;

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
        var lastConstellar = constellars[constellars.Count - 1];
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
                    line.GetComponent<Renderer>().material = new Material(Shader.Find("Custom/SimpleShader"));;
                    guide.line = line;
                    guide.isCreated = true;
                }
            }
        }
    }

    public void SetCreateConstellar()
    {
        Constellar newConstellar = new Constellar();
        constellars.Add(newConstellar);

        createMode = true;
        panelCreate.SetActive(false);
        panelSave.SetActive(true);
    }

    public void SaveConstelars()
    {
        StartCoroutine(SendConstellarData());
        createMode = false;
        panelCreate.SetActive(true);
        panelSave.SetActive(false);
    }

    private IEnumerator SendConstellarData()
    {
        var lastConstellar = constellars[constellars.Count - 1];

        var saveData = new SaveData
        {
            coordenates = new List<string>()
        };

        foreach (var guide in lastConstellar.constellarsGuide)
        {
            saveData.coordenates.Add($"{guide.starA}, {guide.starB}");
        }

        string jsonData = JsonUtility.ToJson(saveData);
        Debug.Log(jsonData);

        UnityWebRequest request = new UnityWebRequest(url, "POST");
        byte[] bodyRaw = Encoding.UTF8.GetBytes(jsonData);
        request.uploadHandler = new UploadHandlerRaw(bodyRaw);
        request.downloadHandler = new DownloadHandlerBuffer();
        request.SetRequestHeader("Content-Type", "application/json");

        yield return request.SendWebRequest();

        if (request.result != UnityWebRequest.Result.Success)
        {
            Debug.Log("Error en la solicitud: " + request.error);
        }
        else
        {
            Debug.Log("Respuesta de la API: " + request.downloadHandler.text);
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
        constellars.Add(new Constellar());
    }

    private IEnumerator GetConstelars()
    {
        var exoplanet = new GetExoplanet
        {
            pl_name = GlobalData.Exoplanets[0].pl_name
        };

        string jsonData = JsonUtility.ToJson(exoplanet);
        UnityWebRequest request = new UnityWebRequest(urlConstellations, "POST");
        byte[] bodyRaw = Encoding.UTF8.GetBytes(jsonData);
        request.uploadHandler = new UploadHandlerRaw(bodyRaw);
        request.downloadHandler = new DownloadHandlerBuffer();
        request.SetRequestHeader("Content-Type", "application/json");

        yield return request.SendWebRequest();

        if (request.result != UnityWebRequest.Result.Success)
        {
            Debug.Log("Error en la solicitud: " + request.error);
        }
        else
        {
            string responseBody = request.downloadHandler.text;
            CreateOldConnections(responseBody);
        }
    }

    public void CreateOldConnections(string oldConstellars)
    {
        var constellarsData = JsonUtility.FromJson<ConstellarDataArray>(oldConstellars);
        Constellar newConstellar = new Constellar();

        foreach (var constellarData in constellarsData.result)
        {
            foreach (var coordinate in constellarData.coordenates)
            {
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

                    guide.line = line;
                    guide.isCreated = true;
                }
            }
        }
    }
}
