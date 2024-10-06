using UnityEngine;
using UnityEngine.SceneManagement;

public class SceneNavigator : MonoBehaviour
{
    public string sceneName; // Nombre de la escena a cargar

    // M�todo que se llama al pulsar el bot�n
    public void LoadScene()
    {
        SceneManager.LoadScene(sceneName);
    }
}
