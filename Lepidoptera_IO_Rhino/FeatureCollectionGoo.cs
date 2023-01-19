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
    public class FeatureCollectionGoo : GH_Goo<FeatureCollection>
    {
        //Constructors
        public FeatureCollectionGoo()
        {
            this.Value = new FeatureCollection();
        }
        public FeatureCollectionGoo(FeatureCollection fc)
        {
            if (fc == null)
            {
                fc = new FeatureCollection();
            }
            this.Value = fc;
        }

        public override IGH_Goo Duplicate()
        {
            return Duplicate();
        }
        public FeatureCollectionGoo DuplicateBoundaryGoo()
        {
            return new FeatureCollectionGoo(Value == null ? new FeatureCollection() : (Lepidoptera.FeatureCollection)Value.Clone());
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
                return $"FeatureCollection: F:{Value.features.Count}";
            }
        }
        public override string TypeName
        {
            get { return ("FeatureCollection"); }
        }
        public override string TypeDescription
        {
            get { return ("Defines a single Lepidoptera FeatureCollection"); }
        }
    }

}
