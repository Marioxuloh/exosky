using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MainCamera : MonoBehaviour
{
    [Header("Movement Settings")]
    public float mainSpeed = 100.0f;  // Velocidad regular
    public float shiftAdd = 250.0f;   // Aumenta al mantener Shift
    public float maxShift = 1000.0f;  // Velocidad m�xima con Shift
    public float camSens = 0.25f;     // Sensibilidad del rat�n

    private Vector3 lastMouse = new Vector3(255, 255, 255); // Posici�n inicial del rat�n
    private bool isDragging = false;  // Controla si se est� arrastrando con el rat�n
    private Camera cam;               // Referencia a la c�mara

    void Start()
    {
        cam = GetComponent<Camera>(); // Obtener la referencia a la c�mara
    }

    void Update()
    {
        // Controlar la rotaci�n solo si se est� arrastrando con el bot�n izquierdo del rat�n
        if (Input.GetMouseButtonDown(0)) // Si se presiona el bot�n izquierdo
        {
            isDragging = true;
            lastMouse = Input.mousePosition; // Guardar la posici�n inicial del rat�n al presionar
        }

        if (Input.GetMouseButtonUp(0)) // Si se suelta el bot�n izquierdo
        {
            isDragging = false;
        }

        if (isDragging)
        {
            Vector3 mouseDelta = Input.mousePosition - lastMouse;
            Vector3 rotation;

            // Comprobar si la c�mara est� en el sur (rotaci�n Z cercana a 180 grados o -180 grados)
            if (Mathf.Abs(transform.eulerAngles.z - 180f) < 1f || Mathf.Abs(transform.eulerAngles.z) > 179f)
            {
                // Invertir tanto el control vertical como horizontal en el sur
                rotation = new Vector3(mouseDelta.y * camSens, -mouseDelta.x * camSens, 0);
            }
            else
            {
                // Controles normales si no est� en el sur
                rotation = new Vector3(-mouseDelta.y * camSens, mouseDelta.x * camSens, 0);
            }

            transform.eulerAngles += rotation; // Aplicar la rotaci�n a la c�mara
            lastMouse = Input.mousePosition;   // Actualizar la �ltima posici�n del rat�n
        }

        // Controlar el movimiento con las teclas
        Vector3 p = GetBaseInput();

        // Controlar el zoom con la rueda del rat�n
        //HandleZoom();
    }

    private Vector3 GetBaseInput()
    {
        Vector3 p_Velocity = new Vector3();
        if (Input.GetKey(KeyCode.W))
        {
            p_Velocity += new Vector3(0, 0, 1);
        }
        if (Input.GetKey(KeyCode.S))
        {
            p_Velocity += new Vector3(0, 0, -1);
        }
        if (Input.GetKey(KeyCode.A))
        {
            p_Velocity += new Vector3(-1, 0, 0);
        }
        if (Input.GetKey(KeyCode.D))
        {
            p_Velocity += new Vector3(1, 0, 0);
        }
        return p_Velocity;
    }

    /*
    private void HandleZoom()
    {
        float scroll = Input.GetAxis("Mouse ScrollWheel");
        if (scroll != 0.0f)
        {
            cam.fieldOfView -= scroll * zoomSpeed;
            cam.fieldOfView = Mathf.Clamp(cam.fieldOfView, minZoom, maxZoom);
        }
    }
    */
}
