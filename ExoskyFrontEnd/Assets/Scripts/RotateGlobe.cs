using UnityEngine;

public class RotateGlobe : MonoBehaviour
{
    public float rotationSpeed = 10f; // Ajusta la velocidad de rotación

    void Update()
    {
        // Usar el scroll del mouse para rotar
        float scrollInput = Input.GetAxis("Mouse ScrollWheel");

        if (scrollInput != 0)
        {
            // Rotar la esfera alrededor del eje Y basado en el scroll del mouse
            transform.Rotate(Vector3.up, scrollInput * rotationSpeed * 100f * Time.deltaTime, Space.World);
        }

        // Detectar el clic del mouse
        if (Input.GetMouseButtonDown(0))
        {
            RaycastHit hit;
            Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);

            if (Physics.Raycast(ray, out hit))
            {
                // Verificar si el objeto clicado tiene el componente CameraSelectionHandler
                CameraSelectionHandler handler = hit.transform.GetComponent<CameraSelectionHandler>();
                if (handler != null)
                {
                    // Llama al método OnPointerClick de CameraSelectionHandler
                    handler.OnPointerClick(null);
                }
            }
        }
    }
}
