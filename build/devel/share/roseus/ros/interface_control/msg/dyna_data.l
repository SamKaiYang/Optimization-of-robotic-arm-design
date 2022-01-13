;; Auto-generated. Do not edit!


(when (boundp 'interface_control::dyna_data)
  (if (not (find-package "INTERFACE_CONTROL"))
    (make-package "INTERFACE_CONTROL"))
  (shadow 'dyna_data (find-package "INTERFACE_CONTROL")))
(unless (find-package "INTERFACE_CONTROL::DYNA_DATA")
  (make-package "INTERFACE_CONTROL::DYNA_DATA"))

(in-package "ROS")
;;//! \htmlinclude dyna_data.msg.html


(defclass interface_control::dyna_data
  :super ros::object
  :slots (_payload _payload_position _vel _acc ))

(defmethod interface_control::dyna_data
  (:init
   (&key
    ((:payload __payload) 0.0)
    ((:payload_position __payload_position) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:vel __vel) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:acc __acc) (make-array 0 :initial-element 0.0 :element-type :float))
    )
   (send-super :init)
   (setq _payload (float __payload))
   (setq _payload_position __payload_position)
   (setq _vel __vel)
   (setq _acc __acc)
   self)
  (:payload
   (&optional __payload)
   (if __payload (setq _payload __payload)) _payload)
  (:payload_position
   (&optional __payload_position)
   (if __payload_position (setq _payload_position __payload_position)) _payload_position)
  (:vel
   (&optional __vel)
   (if __vel (setq _vel __vel)) _vel)
  (:acc
   (&optional __acc)
   (if __acc (setq _acc __acc)) _acc)
  (:serialization-length
   ()
   (+
    ;; float32 _payload
    4
    ;; float32[] _payload_position
    (* 4    (length _payload_position)) 4
    ;; float32[] _vel
    (* 4    (length _vel)) 4
    ;; float32[] _acc
    (* 4    (length _acc)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _payload
       (sys::poke _payload (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32[] _payload_position
     (write-long (length _payload_position) s)
     (dotimes (i (length _payload_position))
       (sys::poke (elt _payload_position i) (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
       )
     ;; float32[] _vel
     (write-long (length _vel) s)
     (dotimes (i (length _vel))
       (sys::poke (elt _vel i) (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
       )
     ;; float32[] _acc
     (write-long (length _acc) s)
     (dotimes (i (length _acc))
       (sys::poke (elt _acc i) (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _payload
     (setq _payload (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32[] _payload_position
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _payload_position (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _payload_position i) (sys::peek buf ptr- :float)) (incf ptr- 4)
     ))
   ;; float32[] _vel
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _vel (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _vel i) (sys::peek buf ptr- :float)) (incf ptr- 4)
     ))
   ;; float32[] _acc
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _acc (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _acc i) (sys::peek buf ptr- :float)) (incf ptr- 4)
     ))
   ;;
   self)
  )

(setf (get interface_control::dyna_data :md5sum-) "c2f6e80701d6dcd8d4e79d9988c813f6")
(setf (get interface_control::dyna_data :datatype-) "interface_control/dyna_data")
(setf (get interface_control::dyna_data :definition-)
      "float32 payload
float32[] payload_position
float32[] vel
float32[] acc
")



(provide :interface_control/dyna_data "c2f6e80701d6dcd8d4e79d9988c813f6")


