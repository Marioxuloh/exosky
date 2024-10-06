using UnityEngine;
using UnityEngine.SceneManagement;

public class SceneNavigator : MonoBehaviour
{
    public string sceneName; // Nombre de la escena a cargar

    // Método que se llama al pulsar el botón
    public void LoadScene()
    {
        SceneManager.LoadScene(sceneName);
    }
}
