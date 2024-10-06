using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;
using UnityEngine.SceneManagement;
using System.Linq; // Para usar Linq y simplificar la búsqueda en listas

public class HoverTextLabel : MonoBehaviour, IPointerEnterHandler, IPointerExitHandler, IPointerClickHandler
{
    // Reference to the panel that will be shown when hovering
    public GameObject panel;

    // Method called when the mouse enters the text label
    public void OnPointerEnter(PointerEventData eventData)
    {
        if (panel != null)
        {
            panel.SetActive(true); // Show the panel when mouse hovers over the text label
        }
    }

    // Method called when the mouse exits the text label
    public void OnPointerExit(PointerEventData eventData)
    {
        if (panel != null)
        {
            panel.SetActive(false); // Hide the panel when mouse leaves the text label
        }
    }

    // Method called when the text label is clicked
    public void OnPointerClick(PointerEventData eventData)
    {
        Text textComponent = GetComponent<Text>();
        if (textComponent != null)
        {
            string selectedPlanetName = textComponent.text;

            // Filtra la lista de exoplanetas para que solo quede el que coincida con el nombre
            GlobalData.Exoplanets = GlobalData.Exoplanets
                                        .Where(exoplanet => exoplanet.pl_name == selectedPlanetName)
                                        .ToList();

            // Cambia a la nueva escena (reemplaza "PlanetDetailsScene" con el nombre de tu escena)
            SceneManager.LoadScene("Select_Angle_Scene");
        }
    }
}
