class GraphicsSettings:
    def __init__(self):
        self.name = ""
        self.ssao_color = 0
        self.dust_params = DustParams()
        self.dynamic_shadow_params = DynamicShadowParams()
        self.fog_params = FogParams()


class DustParams:
    alpha = 0.0
    density = 0.0
    dust_far_distance = 0.0
    dust_near_distance = 0.0
    dust_particle = ""
    dust_size = 0.0


class DynamicShadowParams:
    angle_x = 0.0
    angle_y = 0.0
    light_color = 0
    shadow_color = 0


class FogParams:
    alpha = 0.0
    color = 0
    far_limit = 0.0
    near_limit = 0.0
