using System.Collections;
using System.Collections.Generic;
using Unity.Collections;
using UnityEngine;

public class LorenzSystem : MonoBehaviour
{
    public Transform sphereTransform;
    public float startDelay;


    [Space(10)]
    [SerializeField]
    private double p;
    [SerializeField]
    private double o;
    [SerializeField]
    private double b;
    [SerializeField]
    private int number;

    [Space(10)]
    [SerializeField]
    private int xSplit;
    [SerializeField]
    private int ySplit;
    [SerializeField]
    private int zSplit;

    [Space(10)]
    [SerializeField]
    private double xDiff;
    [SerializeField]
    private double yDiff;
    [SerializeField]
    private double zDiff;


    [Space(10)]
    [SerializeField]
    private double timePerStep;
    [SerializeField]
    private int stepSplit;

    [Space(10)]
    [SerializeField]
    private double initX;
    [SerializeField]
    private double initY;
    [SerializeField]
    private double initZ;

    private double[] x;
    private double[] y;
    private double[] z;

    private Transform[] points;
    private float startTime;
    private bool started;

    // Start is called before the first frame update
    void Start()
    {
        x = new double[number];
        y = new double[number];
        z = new double[number];
        points = new Transform[number];

        for (int i = 0; i < number; ++i)
        {
            x[i] = initX + (i % xSplit) * xDiff;
            y[i] = initY + ((i % zSplit) / ySplit) * xDiff;
            z[i] = initZ + (i / zSplit) * xDiff;

            Color color = Color.HSVToRGB(i / (float)number, 1, 1);
            Color color2 = Color.HSVToRGB(i / (float)number, 0.8f, 1);

            Gradient gradient = new Gradient();
            gradient.SetKeys(
                new GradientColorKey[] { new GradientColorKey(color2, 0.0f), new GradientColorKey(color2, 1.0f) },
                new GradientAlphaKey[] { new GradientAlphaKey(1, 0.0f), new GradientAlphaKey(0, 1.0f) }
            );

            Transform sphereCopy = Instantiate(sphereTransform);
            sphereCopy.GetComponent<Renderer>().material.SetColor("_BaseColor", color);
            sphereCopy.GetComponent<TrailRenderer>().colorGradient = gradient;

            sphereCopy.position = new Vector3((float)x[i], (float)y[i], (float)z[i]);

            points[i] = sphereCopy;


        }

        sphereTransform.gameObject.SetActive(false);
        startTime = Time.time;
    }

    // Update is called once per frame
    void Update()
    {
        if (Time.time < startTime + startDelay)
        {
            return;
        } else if (!started)
        {
            started = true;
            Debug.Log("STARTED", this);
        }
        

        double timeDiff = timePerStep / stepSplit;
        for (int i = 0; i < number; ++i)
        {
            for (int tI = 0; tI < stepSplit; tI++)
            {
                double dx = o * (y[i] - x[i]);
                double dy = x[i] * (p - z[i]) - y[i];
                double dz = x[i] * y[i] - b * z[i];

                x[i] += timeDiff * dx;
                y[i] += timeDiff * dy;
                z[i] += timeDiff * dz;
            }

            points[i].position = new Vector3((float)x[i], (float)y[i], (float)z[i]);
        }
    }
}
