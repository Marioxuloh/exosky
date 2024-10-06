using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;
using System.Security;
using System.Collections;
using UnityEngine.Networking;
using System.Collections.Generic;

[System.Serializable]
public class JsonData
{
    public string name;
}

public class AuthController : MonoBehaviour
{
    public InputField loginUsernameField; // Legacy InputField for username
    public Text errorMessage; // Text for showing error when username is empty
    private string url = "http://127.0.0.1:8000/users/login/";


    public void Continue()
    {
        string username = loginUsernameField.text;

        // Check if the username field is empty
        if (string.IsNullOrEmpty(username))
        {
            errorMessage.gameObject.SetActive(true); // Show error message
        }
        else
        {
            LoginUser(username);

            // Store the username in PlayerPrefs
            PlayerPrefs.SetString("Username", username);
            PlayerPrefs.Save(); // Ensure the data is saved
            
            // Load the next scene, assuming the scene name is "Exoplanet_Selection_Scene"
            SceneManager.LoadScene("Exoplanet_Selection_Scene");
        }
    }


    public void LoginUser(string name)
    {
        StartCoroutine(LoginCoroutine(name));
    }

    private IEnumerator LoginCoroutine(string name)
    {
        Debug.Log("Llamo con " + name);
        // Crear el objeto JSON usando un Dictionarys
        var jsonData = new JsonData
        {
            name = name
        };

        string json = JsonUtility.ToJson(jsonData);

        using (UnityWebRequest request = new UnityWebRequest(url, "POST"))
        {
            byte[] bodyRaw = new System.Text.UTF8Encoding().GetBytes(json);
            request.uploadHandler = new UploadHandlerRaw(bodyRaw);
            request.downloadHandler = new DownloadHandlerBuffer();
            request.SetRequestHeader("Content-Type", "application/json");

            Debug.Log("Env�o con " + bodyRaw);

            // Enviar la solicitud y esperar la respuesta
            yield return request.SendWebRequest();

            Debug.Log("Me quedo " + name);

            // Manejar errores
            if (request.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError("Error: " + request.error);
                Debug.LogError("Response: " + request.downloadHandler.text);
            }
            else
            {
                Debug.Log("Respuesta Login: " + request.downloadHandler.text);
            }

            Debug.Log("Acabo con" + name);

        }
    }
}
