using System;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.SceneManagement;

public class CameraSelectionHandler : MonoBehaviour, IPointerClickHandler
{
    // The number to pass to the next scene
    public int elementNumber; // Set this in the Inspector for each text object

    // This method is called when the text is clicked
    public void OnPointerClick(PointerEventData eventData)
    {
        // Call the method to load the next scene and pass the number
        LoadNextScene(elementNumber);
    }

    private void LoadNextScene(int number)
    {
        // Store the number in PlayerPrefs or a static variable to access in the next scene
        Console.WriteLine(number);
        PlayerPrefs.SetInt("PassedNumber", number);
        PlayerPrefs.Save(); // Save PlayerPrefs

        SceneManager.LoadScene("StarsView");
    }
}
