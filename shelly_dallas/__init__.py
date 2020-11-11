import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import pins
from esphome.const import CONF_ID, CONF_RX_PIN, CONF_TX_PIN

MULTI_CONF = True
AUTO_LOAD = ['sensor']

CONF_ONE_WIRE_ID = 'shelly_on_wire_id'
shelly_dallas_ns = cg.esphome_ns.namespace('shelly_dallas')
DallasComponent = shelly_dallas_ns.class_('DallasComponent', cg.PollingComponent)
ShellyOneWire = shelly_dallas_ns.class_('ShellyOneWire')

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(DallasComponent),
    cv.GenerateID(CONF_ONE_WIRE_ID): cv.declare_id(ShellyOneWire),
    cv.Required(CONF_RX_PIN): pins.gpio_input_pin_schema,
    cv.Required(CONF_TX_PIN): pins.gpio_output_pin_schema,
}).extend(cv.polling_component_schema('60s'))


def to_code(config):
    input_pin = yield cg.gpio_pin_expression(config[CONF_RX_PIN])
    output_pin = yield cg.gpio_pin_expression(config[CONF_TX_PIN])
    one_wire = cg.new_Pvariable(config[CONF_ONE_WIRE_ID], input_pin, output_pin)
    var = cg.new_Pvariable(config[CONF_ID], one_wire)
    yield cg.register_component(var, config)
