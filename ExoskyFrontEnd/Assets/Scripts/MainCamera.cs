using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MainCamera : MonoBehaviour
{
    [Header("Movement Settings")]
    public float mainSpeed = 100.0f;  // Velocidad regular
    public float shiftAdd = 250.0f;   // Aumenta al mantener Shift
    public float maxShift = 1000.0f;  // Velocidad máxima con Shift
    public float camSens = 0.25f;     // Sensibilidad del ratón

    private Vector3 lastMouse = new Vector3(255, 255, 255); // Posición inicial del ratón
    private bool isDragging = false;  // Controla si se está arrastrando con el ratón
    private Camera cam;               // Referencia a la cámara

    void Start()
    {
        cam = GetComponent<Camera>(); // Obtener la referencia a la cámara
    }

    void Update()
    {
        // Controlar la rotación solo si se está arrastrando con el botón izquierdo del ratón
        if (Input.GetMouseButtonDown(0)) // Si se presiona el botón izquierdo
        {
            isDragging = true;
            lastMouse = Input.mousePosition; // Guardar la posición inicial del ratón al presionar
        }

        if (Input.GetMouseButtonUp(0)) // Si se suelta el botón izquierdo
        {
            isDragging = false;
        }

        if (isDragging)
        {
            Vector3 mouseDelta = Input.mousePosition - lastMouse;
            Vector3 rotation;

            // Comprobar si la cámara está en el sur (rotación Z cercana a 180 grados o -180 grados)
            if (Mathf.Abs(transform.eulerAngles.z - 180f) < 1f || Mathf.Abs(transform.eulerAngles.z) > 179f)
            {
                // Invertir tanto el control vertical como horizontal en el sur
                rotation = new Vector3(mouseDelta.y * camSens, -mouseDelta.x * camSens, 0);
            }
            else
            {
                // Controles normales si no está en el sur
                rotation = new Vector3(-mouseDelta.y * camSens, mouseDelta.x * camSens, 0);
            }

            transform.eulerAngles += rotation; // Aplicar la rotación a la cámara
            lastMouse = Input.mousePosition;   // Actualizar la última posición del ratón
        }

        // Controlar el movimiento con las teclas
        Vector3 p = GetBaseInput();
        if (p.sqrMagnitude > 0)
        {
            if (Input.GetKey(KeyCode.LeftShift))
            {
                p = p * shiftAdd;
                p.x = Mathf.Clamp(p.x, -maxShift, maxShift);
                p.y = Mathf.Clamp(p.y, -maxShift, maxShift);
                p.z = Mathf.Clamp(p.z, -maxShift, maxShift);
            }
            else
            {
                p = p * mainSpeed;
            }

            p = p * Time.deltaTime;
            transform.Translate(p);
        }

        // Controlar el zoom con la rueda del ratón
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
