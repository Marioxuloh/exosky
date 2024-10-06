using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.UI;
using System.Linq;
using UnityEngine.SceneManagement;

[System.Serializable]
public class SearchBarJsonData
{
    public string pl_name;
}

public class SearchBar : MonoBehaviour
{
    public InputField searchInputField; // Assign the InputField from the inspector
    public Button searchButton; // Assign the Button from the inspector
    public Text feedbackText; // Text component to display feedback messages (optional)
    private string url = "http://127.0.0.1:8000/exoplanets/getbyname/"; // Replace with your backend URL

    private void Start()
    {
        // Add a listener to the button to call the Search function when clicked
        searchButton.onClick.AddListener(Search);
    }

    public void Search()
    {
        // Check if the input field text is null or empty/whitespace
        if (string.IsNullOrWhiteSpace(searchInputField.text))
        {
            if (feedbackText != null)
            {
                feedbackText.gameObject.SetActive(true);
                feedbackText.text = "You have to introduce some name.";
            }
            return; // Exit the method if the input is invalid
        }

        // Get the text from the InputField
        string searchText = searchInputField.text;

        // Call the function to perform the search
        StartCoroutine(SearchInBackend(searchText));
    }

    private IEnumerator SearchInBackend(string searchText)
    {
        var jsonData = new SearchBarJsonData { pl_name = searchText };
        string json = JsonUtility.ToJson(jsonData);

        // Crear la solicitud POST
        using (UnityWebRequest request = new UnityWebRequest(url, "POST"))
        {
            byte[] bodyRaw = new System.Text.UTF8Encoding().GetBytes(json);
            request.uploadHandler = new UploadHandlerRaw(bodyRaw);
            request.downloadHandler = new DownloadHandlerBuffer();
            request.SetRequestHeader("Content-Type", "application/json");

            // Enviar la solicitud y esperar la respuesta
            yield return request.SendWebRequest();

            // Manejar errores
            if (request.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError("Error: " + request.error);
                Debug.LogError("Response: " + request.downloadHandler.text);
                if (feedbackText != null)
                {
                    feedbackText.gameObject.SetActive(true);
                    feedbackText.text = "The exoplanet doesn`t exist. Try again.";
                }
            }
            else
            {
                // Deserializar el JSON a una lista de objetos Exoplanet
                Exoplanet exoplanet = JsonHelper.SingleFromJson<Exoplanet>(request.downloadHandler.text);

                Debug.Log(exoplanet);
                
                if (exoplanet == null)
                {
                    searchInputField.text = "";
                    feedbackText.gameObject.SetActive(true);
                    feedbackText.text = "The exoplanet doesn`t exist. Try again.";
                }else
                {
                    Debug.Log(exoplanet.pl_name);
                    exoplanet.material = Resources.Load<Material>("RandomTextures/New Material 5");

                    GlobalData.Exoplanets.Clear(); // Limpiar la lista antes de agregar nuevos datos
                    GlobalData.Exoplanets.Add(exoplanet); // Agregar los nuevos exoplanetas
                    Debug.Log("Datos guardados: " + GlobalData.Exoplanets[0].pl_name);
                    SceneManager.LoadScene("Select_Angle_Scene");
                }

                
            }
        }
    }
}
