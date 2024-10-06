using UnityEngine;

public static class JsonHelper
{
    public static T[] FromJson<T>(string json)
    {
        string newJson = "{ \"array\": " + json + "}";
        Wrapper<T> wrapper = JsonUtility.FromJson<Wrapper<T>>(newJson);
        return wrapper.array;
    }

    public static T SingleFromJson<T>(string json)
    {
        return JsonUtility.FromJson<T>(json);
    }

    [System.Serializable]
    private class Wrapper<T>
    {
        public T[] array;
    }
}
