import torch


class IncidentForecasterPT:
    def forecast_impact(self,severity:str)->dict:
        severity_mapping={"Low": 1.0, "Medium": 2.0, "High": 3.0, "Critical": 4.0}
        val=severity_mapping.get(severity,2.0)
        input_tensor=torch.tensor([val],dtype=torch.float32)
        weights=torch.tensor([2.5,1.2])
        bias=torch.tensor([1.0,0.5])
        output_tensor = (input_tensor * weights) + bias
        estimated_hours = round(float(output_tensor[0]), 1)
        impact_radius_km = round(float(output_tensor[1]), 1)
        data_used={
            "input tensor":input_tensor.tolist(),
            "output tensor":output_tensor.tolist(),
            "device":str(input_tensor.device)
        }
        return {
            "estimated resolution hours":estimated_hours,
            "impact radius km":impact_radius_km,
            "pt data context": data_used
        }