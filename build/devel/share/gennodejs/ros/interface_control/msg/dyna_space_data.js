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

class dyna_space_data {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.payload = null;
      this.payload_position = null;
      this.vel = null;
      this.acc = null;
      this.joint_limits = null;
      this.analysis_axis = null;
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
      if (initObj.hasOwnProperty('joint_limits')) {
        this.joint_limits = initObj.joint_limits
      }
      else {
        this.joint_limits = [];
      }
      if (initObj.hasOwnProperty('analysis_axis')) {
        this.analysis_axis = initObj.analysis_axis
      }
      else {
        this.analysis_axis = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type dyna_space_data
    // Serialize message field [payload]
    bufferOffset = _serializer.float64(obj.payload, buffer, bufferOffset);
    // Serialize message field [payload_position]
    bufferOffset = _arraySerializer.float32(obj.payload_position, buffer, bufferOffset, null);
    // Serialize message field [vel]
    bufferOffset = _arraySerializer.float32(obj.vel, buffer, bufferOffset, null);
    // Serialize message field [acc]
    bufferOffset = _arraySerializer.float32(obj.acc, buffer, bufferOffset, null);
    // Serialize message field [joint_limits]
    bufferOffset = _arraySerializer.float32(obj.joint_limits, buffer, bufferOffset, null);
    // Serialize message field [analysis_axis]
    bufferOffset = _serializer.int32(obj.analysis_axis, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type dyna_space_data
    let len;
    let data = new dyna_space_data(null);
    // Deserialize message field [payload]
    data.payload = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [payload_position]
    data.payload_position = _arrayDeserializer.float32(buffer, bufferOffset, null)
    // Deserialize message field [vel]
    data.vel = _arrayDeserializer.float32(buffer, bufferOffset, null)
    // Deserialize message field [acc]
    data.acc = _arrayDeserializer.float32(buffer, bufferOffset, null)
    // Deserialize message field [joint_limits]
    data.joint_limits = _arrayDeserializer.float32(buffer, bufferOffset, null)
    // Deserialize message field [analysis_axis]
    data.analysis_axis = _deserializer.int32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 4 * object.payload_position.length;
    length += 4 * object.vel.length;
    length += 4 * object.acc.length;
    length += 4 * object.joint_limits.length;
    return length + 28;
  }

  static datatype() {
    // Returns string type for a message object
    return 'interface_control/dyna_space_data';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '505831417ccc6ae5a2e31ba38a82a2b6';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float64 payload
    float32[] payload_position
    float32[] vel
    float32[] acc
    float32[] joint_limits
    int32 analysis_axis
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new dyna_space_data(null);
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

    if (msg.joint_limits !== undefined) {
      resolved.joint_limits = msg.joint_limits;
    }
    else {
      resolved.joint_limits = []
    }

    if (msg.analysis_axis !== undefined) {
      resolved.analysis_axis = msg.analysis_axis;
    }
    else {
      resolved.analysis_axis = 0
    }

    return resolved;
    }
};

module.exports = dyna_space_data;
