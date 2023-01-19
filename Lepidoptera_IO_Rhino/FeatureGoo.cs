using System.Collections.Generic;
using Rhino;
using Rhino.Geometry;
using Grasshopper;
using Grasshopper.Kernel;
using Grasshopper.Kernel.Data;
using Grasshopper.Kernel.Types;
using Lepidoptera;

namespace Lepidoptera
{

    /// <summary>
    /// Tier Goo wrapper class, makes sure Tier can be used in Grasshopper.
    /// </summary>
    public class FeatureGoo : GH_Goo<Feature>
    {
        //Constructors
        public FeatureGoo()
        {
            this.Value = new Feature();
        }
        public FeatureGoo(Feature feature)
        {
            if (feature == null)
            {
                feature = new Feature();
            }
            this.Value = feature;
        }

        public override IGH_Goo Duplicate()
        {
            return Duplicate();
        }
        public FeatureGoo DuplicateBoundaryGoo()
        {
            return new FeatureGoo(Value == null ? new Feature() : (Lepidoptera.Feature)Value.Clone());
        }

        public override bool IsValid
        {
            get
            {
                if (Value == null) { return false; }
                return Value.IsValid;
            }
        }

        public override string ToString()
        {
            if (Value == null)
            {
                return "Null FeatureCollection";
            }
            else
            {
                return $"Feature: B1:{Value.properties.B1}";
            }
        }
        public override string TypeName
        {
            get { return ("FeatureCollection"); }
        }
        public override string TypeDescription
        {
            get { return ("Defines a single Lepidoptera Feature"); }
        }
    }

}
