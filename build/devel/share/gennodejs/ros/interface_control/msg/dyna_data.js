// Auto-generated. Do not edit!

// (in-package interface_control.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class dyna_data {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.payload = null;
      this.payload_position = null;
      this.vel = null;
      this.acc = null;
    }
    else {
      if (initObj.hasOwnProperty('payload')) {
        this.payload = initObj.payload
      }
      else {
        this.payload = 0.0;
      }
      if (initObj.hasOwnProperty('payload_position')) {
        this.payload_position = initObj.payload_position
      }
      else {
        this.payload_position = [];
      }
      if (initObj.hasOwnProperty('vel')) {
        this.vel = initObj.vel
      }
      else {
        this.vel = [];
      }
      if (initObj.hasOwnProperty('acc')) {
        this.acc = initObj.acc
      }
      else {
        this.acc = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type dyna_data
    // Serialize message field [payload]
    bufferOffset = _serializer.float32(obj.payload, buffer, bufferOffset);
    // Serialize message field [payload_position]
    bufferOffset = _arraySerializer.float32(obj.payload_position, buffer, bufferOffset, null);
    // Serialize message field [vel]
    bufferOffset = _arraySerializer.float32(obj.vel, buffer, bufferOffset, null);
    // Serialize message field [acc]
    bufferOffset = _arraySerializer.float32(obj.acc, buffer, bufferOffset, null);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type dyna_data
    let len;
    let data = new dyna_data(null);
    // Deserialize message field [payload]
    data.payload = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [payload_position]
    data.payload_position = _arrayDeserializer.float32(buffer, bufferOffset, null)
    // Deserialize message field [vel]
    data.vel = _arrayDeserializer.float32(buffer, bufferOffset, null)
    // Deserialize message field [acc]
    data.acc = _arrayDeserializer.float32(buffer, bufferOffset, null)
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 4 * object.payload_position.length;
    length += 4 * object.vel.length;
    length += 4 * object.acc.length;
    return length + 16;
  }

  static datatype() {
    // Returns string type for a message object
    return 'interface_control/dyna_data';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'c2f6e80701d6dcd8d4e79d9988c813f6';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float32 payload
    float32[] payload_position
    float32[] vel
    float32[] acc
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new dyna_data(null);
    if (msg.payload !== undefined) {
      resolved.payload = msg.payload;
    }
    else {
      resolved.payload = 0.0
    }

    if (msg.payload_position !== undefined) {
      resolved.payload_position = msg.payload_position;
    }
    else {
      resolved.payload_position = []
    }

    if (msg.vel !== undefined) {
      resolved.vel = msg.vel;
    }
    else {
      resolved.vel = []
    }

    if (msg.acc !== undefined) {
      resolved.acc = msg.acc;
    }
    else {
      resolved.acc = []
    }

    return resolved;
    }
};

module.exports = dyna_data;
