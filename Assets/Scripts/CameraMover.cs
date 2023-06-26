using System.Collections;
using System.Collections.Generic;
using Unity.VisualScripting;
using UnityEngine;

[RequireComponent(typeof(Camera))]
public class CameraMover : MonoBehaviour
{
    public float speed;
    public float rotSpeed;
    private Dictionary<KeyCode, Vector3> directions;
    private Camera camera;

    private bool movementMode;
    private Vector3 rotVector;
    private Quaternion rotQuart;

    // Start is called before the first frame update
    void Start()
    {
        directions = new Dictionary<KeyCode, Vector3>();
        
        directions[KeyCode.D] = Vector3.right;
        directions[KeyCode.A] = Vector3.left;
        
        directions[KeyCode.W] = Vector3.up;
        directions[KeyCode.S] = Vector3.down;

        directions[KeyCode.Q] = Vector3.forward;
        directions[KeyCode.E] = Vector3.back;

        camera = GetComponent<Camera>();
        movementMode = true;
    }

    // Update is called once per frame
    void Update()
    {
        Vector3 movementVector = Vector3.zero;    

        foreach (KeyCode key in directions.Keys)
        {
            if (Input.GetKey(key))
            {
                movementVector += directions[key];
            }
        }

        if (Input.GetKeyDown(KeyCode.K))
        {
            movementMode = !movementMode ;
        }

        if (movementMode)
        {
            transform.position = camera.transform.TransformPoint(movementVector * Time.deltaTime * speed);
        } else
        {
            //camera.transform.LookAt(movementVector * rotSpeed, Vector3.up);
            if (movementVector != Vector3.zero)
            {
                movementVector = movementVector * Mathf.PI / 180f;
                rotVector += movementVector;
                float sinTheta = Mathf.Sin(rotVector.x);
                float cosTheta = Mathf.Cos(rotVector.x);

                float sinPhi = Mathf.Sin(rotVector.y);
                float cosPhi = Mathf.Cos(rotVector.y);

                Vector3 lookAtVector = new Vector3(sinPhi * cosTheta, sinPhi * sinTheta, cosPhi);

                rotQuart = Quaternion.LookRotation(lookAtVector, Vector3.up);
                transform.rotation = Quaternion.Slerp(transform.rotation, rotQuart, Time.deltaTime);
            }
        }
    }
}
