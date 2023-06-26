using System;
using UnityEditor;
using UnityEngine;

public class SinglePendulumMultiple : MonoBehaviour
{
    public Transform pivot;
    public Transform pendulum;
    public Transform phaseSpace;
    public Transform phasePointObject;

    [SerializeField]
    private double maxVelocity;
    [SerializeField]
    private double maxAngle;

    public double gravity;

    [SerializeField]
    private double timePerStep;
    [SerializeField]
    private int stepSplit;
    [SerializeField]
    private double startAngle;
    [SerializeField]
    private double angleDelta;

    [SerializeField]
    private double drag;

    [SerializeField]
    private int pendulumCount;

    private double pendulumLength;
    
    private double[] theta; // Angle
    private double[] omega; // Angular Velocity
    private double[] alpha; // Angular Acceleration
    private Transform[] pendulumObjects;
    private Transform[] phasePoints;
    // Debug Info
    private double maxX;
    private double maxV;

    private float sizeX;

    double calculateAlpha(double angle)
    {
        return - gravity / pendulumLength * Math.Sin(angle);
    }

    Vector3 angleVector(double angle)
    {
        return new Vector3((float)Math.Sin(angle), -(float)Math.Cos(angle), 0);
    }

    void UpdatePendulums()
    {
        for (int i = 0; i < pendulumObjects.Length; ++i)
        {
            pendulumObjects[i].position = pivot.position + (float)pendulumLength*angleVector(theta[i]);
            if (pendulumObjects[i].position.x > maxX)
            {
                maxX = pendulumObjects[i].position.x;
            }
        }
    }

    // Start is called before the first frame update
    void Start()
    {
        sizeX = 10;
        maxX = 0;
        pendulumLength = (pivot.position - pendulum.position).magnitude;

        theta = new double[pendulumCount];
        omega = new double[pendulumCount];
        alpha = new double[pendulumCount];
        pendulumObjects = new Transform[pendulumCount];
        phasePoints = new Transform[pendulumCount];

        for (int i = 0; i < theta.Length; i++)
        {
            theta[i] = startAngle + i * angleDelta;
            omega[i] = 0;
            alpha[i] = 0;

            Color color = Color.HSVToRGB(i / (float)pendulumCount, 1, 1);
            Color color2 = Color.HSVToRGB(i / (float)pendulumCount, 0.8f, 1);

            Gradient gradient = new Gradient();
            gradient.SetKeys(
                new GradientColorKey[] { new GradientColorKey(color2, 0.0f), new GradientColorKey(color2, 1.0f) },
                new GradientAlphaKey[] { new GradientAlphaKey(1, 0.0f), new GradientAlphaKey(0, 1.0f) }
            );

            Transform newPendulum = Instantiate(pendulum);
            newPendulum.GetComponent<Renderer>().material.SetColor("_BaseColor", color);
            pendulumObjects[i] = newPendulum;

            Transform newPhasePoint = Instantiate(phasePointObject);
            newPhasePoint.GetComponent<Renderer>().material.SetColor("_BaseColor", color);
            newPhasePoint.GetComponent<TrailRenderer>().colorGradient = gradient;

            newPhasePoint.parent = phaseSpace;
            newPhasePoint.localPosition = Vector3.zero;
            phasePoints[i] = newPhasePoint;
        }

        pendulum.gameObject.SetActive(false);
        phasePointObject.gameObject.SetActive(false);
    }

    void FixedUpdate()
    {
        double stepTime = timePerStep / (double)stepSplit;
        for (int i = 0; i < alpha.Length; ++i)
        {
            for (int i2 = 0; i2 < stepSplit; ++i2)
            {
                alpha[i] = calculateAlpha(theta[i]) - drag*Math.Pow(omega[i], 2) * Math.Sign(omega[i]);
                
                // Euler (Small Time Period)    
                omega[i] += alpha[i] * stepTime;
                theta[i] += omega[i] * stepTime;
                phasePoints[i].localPosition = new Vector3((float)(theta[i] / maxAngle * sizeX / 2f), 1, (float)(omega[i] / maxVelocity * sizeX / 2f));

                maxV = Math.Max(maxX, omega[i]);
            }
        }

        UpdatePendulums();
    }

    private void OnDrawGizmos()
    {
        //Gizmos.DrawLine(pivot.position, pendulum.position);
        for (int i = 0; i < pendulumObjects.Length; ++i)
        {
            Gizmos.DrawLine(pivot.position, pendulumObjects[i].position);
        }
        Gizmos.DrawLine(new Vector3((float)maxX, -10, -9), new Vector3((float)maxX, 10, -9));
        //Handles.Label(pivot.position, $"{maxV}");
    }
}
