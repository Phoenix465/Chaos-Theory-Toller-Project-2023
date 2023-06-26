using UnityEditor;
using UnityEngine;
using System;

public class DoublePendulumMultiple : MonoBehaviour
{
    public Transform pivot;
    public Transform pendulum1;
    public Transform pendulum2;

    public Transform phaseSpace;
    public Transform phaseSpace3D;
    public Transform phasePointObject;

    public double gravity;

    public DPEnums XAxis;
    public DPEnums YAxis;
    public DPEnums ZAxis;
    public DPEnums ColourEnum;

    public bool modAngles;

    [SerializeField]
    private double maxVelocity;
    [SerializeField]
    private double maxAngle;

    [SerializeField]
    private double timePerStep;
    [SerializeField]
    private int stepSplit;
    [SerializeField]
    private double startAngle1;
    [SerializeField]
    private double startAngle2;
    [SerializeField]
    private double angleDelta;

    [SerializeField]
    private double drag;

    [SerializeField]
    private double mass1;
    [SerializeField]
    private double mass2;

    [SerializeField]
    private int pendulumCount;

    private double length1;
    private double length2;

    private double[] theta1; // Angle 1
    private double[] theta2; // Angle 2

    private double[] omega1; // Angular Velocity 1
    private double[] omega2; // Angular Velocity 2

    private double[] alpha1; // Angular Acceleration 1
    private double[] alpha2; // Angular Acceleration 2

    private Transform[] pendulumObjects1;
    private LineRenderer[] pendulumObjects1LineRenderer;
    private LineRenderer[] pendulumObjects2LineRenderer;

    private Transform[] pendulumObjects2;
    private Transform[] phasePoints;
    private Transform[] phasePoints3D;

    // Debug Info
    private double maxX;
    private double maxV;

    private float sizeX;


    double calculateAlpha1(double angle1, double aVelocity1, double angle2, double aVelocity2)
    {
        return (-gravity * (2 * mass1 + mass2) * Math.Sin(angle1) - mass2 * gravity * Math.Sin(angle1 - 2 * angle2) - 2*Math.Sin(angle1 - angle2) * mass2 * (Math.Pow(aVelocity2, 2)*length2 + Math.Pow(aVelocity1, 2)*length1 * Math.Cos(angle1 - angle2))) / (length1 * (2*mass1 + mass2 - mass2 * (Math.Cos(2 * angle1 - 2 * angle2))));
    }

    double calculateAlpha2(double angle1, double aVelocity1, double angle2, double aVelocity2)
    {
        return (2 * Math.Sin(angle1 - angle2) * (Math.Pow(aVelocity1, 2) * length1 * (mass1 + mass2) + gravity * (mass1 + mass2)*Math.Cos(angle1) + (Math.Pow(aVelocity2, 2) * length2 * mass2 * Math.Cos(angle1 - angle2)))) / (length2 * (2 * mass1 + mass2 - mass2 * (Math.Cos(2 * angle1 - 2 * angle2))));
    }

    Vector3 angleVector(double angle)
    {
        return new Vector3((float)Math.Sin(angle), -(float)Math.Cos(angle), 0);
    }

    double getData(DPEnums dpEnum, int i)
    {
        switch (dpEnum)
        {
            case DPEnums.Theta1:
                return theta1[i];
            case DPEnums.Theta2:
                return theta2[i];
            case DPEnums.Omega1:
                return theta2[i];
            case DPEnums.Omega2:
                return omega2[i];
            case DPEnums.Number:
                return i;
            default:
                return 0;
        }
    }

    double getMaxValue(DPEnums dpEnum)
    {
        switch (dpEnum)
        {
            case DPEnums.Theta1:
                return maxAngle;
            case DPEnums.Theta2:
                return maxAngle;
            case DPEnums.Omega1:
                return maxVelocity;
            case DPEnums.Omega2:
                return maxVelocity;
            case DPEnums.Number:
                return pendulumCount;
            default:
                return 1;
        }
    }

    void UpdatePendulums()
    {
        for (int i = 0; i < pendulumObjects1.Length; ++i)
        {
            pendulumObjects1[i].position = pivot.position + (float)length1 * angleVector(theta1[i]);
            pendulumObjects2[i].position = pendulumObjects1[i].position + (float)length2 * angleVector(theta2[i]);
            if (pendulumObjects1[i].position.x > maxX)
            {
                maxX = pendulumObjects1[i].position.x;
            }

            phasePoints[i].localPosition = new Vector3((float)(theta1[i] / maxAngle * sizeX / 2f), 1, (float)(theta2[i] / maxAngle * sizeX / 2f));

            pendulumObjects1LineRenderer[i].SetPosition(1, pendulumObjects1[i].position);

            pendulumObjects2LineRenderer[i].SetPosition(0, pendulumObjects1[i].position);
            pendulumObjects2LineRenderer[i].SetPosition(1, pendulumObjects2[i].position);


            double xAxisVal = getData(XAxis, i);
            double yAxisVal = getData(YAxis, i);
            double zAxisVal = getData(ZAxis, i);
            double colourVal = getData(ColourEnum, i);

            double maxXVal = getMaxValue(XAxis);
            double maxYVal = getMaxValue(YAxis);
            double maxZVal = getMaxValue(ZAxis);
            double maxColourVal = getMaxValue(ColourEnum);

            phasePoints3D[i].localPosition = new Vector3(
                 (float)(xAxisVal / maxXVal * sizeX / 2f),
                 (float)(zAxisVal / maxZVal * sizeX / 2f),
                 (float)(yAxisVal / maxYVal * sizeX / 2f)
            );

            Transform pp3d = phasePoints3D[i];

            Color color, color2;
            if (ColourEnum == DPEnums.Number)
            {
                color = Color.HSVToRGB(i / (float)pendulumCount, 1, 1);
                color2 = Color.HSVToRGB(i / (float)pendulumCount, 0.8f, 1);
            }
            else
            {

                color = Color.HSVToRGB((float)(colourVal / maxColourVal) % 1, 1, 1);
                color2 = Color.HSVToRGB((float)(colourVal / maxColourVal) % 1, 0.8f, 1);
            }

            Gradient gradient = new Gradient();
            gradient.SetKeys(
                new GradientColorKey[] { new GradientColorKey(color2, 0.0f), new GradientColorKey(color2, 1.0f) },
                new GradientAlphaKey[] { new GradientAlphaKey(1, 0.0f), new GradientAlphaKey(0, 1.0f) }
            );

            pp3d.GetComponent<Renderer>().material.SetColor("_BaseColor", color);
            pp3d.GetComponent<TrailRenderer>().colorGradient = gradient;
        }
    }

    // Start is called before the first frame update
    void Start()
    {
        sizeX = 10;

        maxX = 0;
        length1 = (pivot.position - pendulum1.position).magnitude;
        length2 = (pendulum1.position - pendulum2.position).magnitude;

        theta1 = new double[pendulumCount];
        omega1 = new double[pendulumCount];
        alpha1 = new double[pendulumCount];

        theta2 = new double[pendulumCount];
        omega2 = new double[pendulumCount];
        alpha2 = new double[pendulumCount];

        pendulumObjects1 = new Transform[pendulumCount];
        pendulumObjects1LineRenderer = new LineRenderer[pendulumCount];
        pendulumObjects2LineRenderer = new LineRenderer[pendulumCount];
        pendulumObjects2 = new Transform[pendulumCount];
        phasePoints = new Transform[pendulumCount];
        phasePoints3D = new Transform[pendulumCount];


        for (int i = 0; i < theta1.Length; i++)
        {
            theta1[i] = startAngle1 + i * angleDelta;
            omega1[i] = 0;
            alpha1[i] = 0;

            theta2[i] = startAngle2 ;
            omega2[i] = 0;
            alpha2[i] = 0;

            Color color = Color.HSVToRGB(i / (float)pendulumCount, 1, 1);
            Color color2 = Color.HSVToRGB(i / (float)pendulumCount, 0.8f, 1);

            Gradient gradient = new Gradient();
            gradient.SetKeys(
                new GradientColorKey[] { new GradientColorKey(color2, 0.0f), new GradientColorKey(color2, 1.0f) },
                new GradientAlphaKey[] { new GradientAlphaKey(1, 0.0f), new GradientAlphaKey(0, 1.0f) }
            );

            Gradient gradient2 = new Gradient();
            gradient2.SetKeys(
                new GradientColorKey[] { new GradientColorKey(color2, 0.0f), new GradientColorKey(color2, 0.0f) },
                new GradientAlphaKey[] { new GradientAlphaKey(1, 0.0f), new GradientAlphaKey(0, 0.0f) }
            );

            Transform newPendulum1 = Instantiate(pendulum1);
            Transform newPendulum2 = Instantiate(pendulum2);

            newPendulum1.GetComponent<Renderer>().material.SetColor("_BaseColor", color);
            newPendulum2.GetComponent<Renderer>().material.SetColor("_BaseColor", color);

            pendulumObjects1[i] = newPendulum1;
            pendulumObjects2[i] = newPendulum2;

            pendulumObjects1LineRenderer[i] = newPendulum1.GetComponent<LineRenderer>();
            pendulumObjects1LineRenderer[i].positionCount = 2;
            pendulumObjects1LineRenderer[i].SetPosition(0, pivot.position);
            pendulumObjects1LineRenderer[i].colorGradient = gradient2;

            pendulumObjects2LineRenderer[i] = newPendulum2.GetComponent<LineRenderer>();
            pendulumObjects2LineRenderer[i].positionCount = 2;
            pendulumObjects2LineRenderer[i].colorGradient = gradient2;

            Transform newPhasePoint = Instantiate(phasePointObject);
            newPhasePoint.GetComponent<Renderer>().material.SetColor("_BaseColor", color);
            newPhasePoint.GetComponent<TrailRenderer>().colorGradient = gradient;

            newPhasePoint.parent = phaseSpace;
            newPhasePoint.localPosition = Vector3.zero;
            phasePoints[i] = newPhasePoint;

            Transform newPhasePoint2 = Instantiate(phasePointObject);
            newPhasePoint2.GetComponent<Renderer>().material.SetColor("_BaseColor", color);
            newPhasePoint2.GetComponent<TrailRenderer>().colorGradient = gradient;

            newPhasePoint2.parent = phaseSpace3D;
            newPhasePoint2.localPosition = Vector3.zero;
            phasePoints3D[i] = newPhasePoint2;
        }

        pendulum1.gameObject.SetActive(false);
        pendulum2.gameObject.SetActive(false);
        phasePointObject.gameObject.SetActive(false);
    }

    void FixedUpdate()
    {
        double stepTime = timePerStep / (double)stepSplit;
        for (int i = 0; i < alpha1.Length; ++i)
        {
            for (int i2 = 0; i2 < stepSplit; ++i2)
            {
                alpha1[i] = calculateAlpha1(theta1[i], omega1[i], theta2[i], omega2[i]);
                alpha2[i] = calculateAlpha2(theta1[i], omega1[i], theta2[i], omega2[i]);

                // Euler
                omega1[i] += alpha1[i] * stepTime;
                omega2[i] += alpha2[i] * stepTime;

                theta1[i] += omega1[i] * stepTime;
                theta2[i] += omega2[i] * stepTime;
            }

            if (modAngles)
            {
                theta1[i] = theta1[i] % (double)(2 * Mathf.PI);
                theta2[i] = theta2[i] % (double)(2 * Mathf.PI);
            }
        }

        UpdatePendulums();
    }
}
