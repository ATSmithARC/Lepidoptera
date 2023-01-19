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
    public class FeatureTableGoo : GH_Goo<FeatureTable>
    {
        //Constructors
        public FeatureTableGoo()
        {
            this.Value = new FeatureTable();
        }
        public FeatureTableGoo(FeatureTable ft)
        {
            if (ft == null)
            {
                ft = new FeatureTable();
            }
            this.Value = ft;
        }

        public override IGH_Goo Duplicate()
        {
            return Duplicate();
        }
        public FeatureTableGoo DuplicateBoundaryGoo()
        {
            return new FeatureTableGoo(Value == null ? new FeatureTable() : (Lepidoptera.FeatureTable)Value.Clone());
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
                return "Null FeatureTable";
            }
            else
            {
                return $"FeatureTable: T:{Value.Type} C:{Value.Features.Columns.Count} R:{Value.Features.Rows.Count}";
            }
        }
        public override string TypeName
        {
            get { return ("FeatureCollection"); }
        }
        public override string TypeDescription
        {
            get { return ("Defines a single Lepidoptera FeatureTable"); }
        }
    }

}
