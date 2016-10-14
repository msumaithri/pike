import pike.core as core
import pike.model as model
import pike.smb2 as smb2
import pike.test

class TestClientCallbacks(pike.test.PikeTest):
    def test_pre_serialize(self):
        callback_future = model.Future()
        def cb(frame):
            with callback_future:
                self.assertTrue(isinstance(frame, core.Frame))
                self.assertTrue(isinstance(frame[0], smb2.Smb2))
                self.assertTrue(isinstance(frame[0][0], smb2.NegotiateRequest))
                self.assertFalse(hasattr(frame, "buf"))
                callback_future.complete(True)
        self.default_client.register_callback(model.EV_REQ_PRE_SERIALIZE, cb)
        conn = self.default_client.connect(self.server)
        conn.negotiate()
        self.assertTrue(callback_future.result(timeout=2))

    def test_post_serialize(self):
        callback_future = model.Future()
        def cb(frame):
            with callback_future:
                self.assertTrue(isinstance(frame, core.Frame))
                self.assertTrue(isinstance(frame[0], smb2.Smb2))
                self.assertTrue(isinstance(frame[0][0], smb2.NegotiateRequest))
                self.assertTrue(hasattr(frame, "buf"))
                self.assertEqual(frame.len + 4, len(frame.buf))
                callback_future.complete(True)
        self.default_client.register_callback(model.EV_REQ_POST_SERIALIZE, cb)
        conn = self.default_client.connect(self.server)
        conn.negotiate()
        self.assertTrue(callback_future.result(timeout=2))

    def test_pre_deserialize(self):
        callback_future = model.Future()
        def cb(data):
            with callback_future:
                self.assertGreater(len(data), 0)
                callback_future.complete(True)
        self.default_client.register_callback(model.EV_RES_PRE_DESERIALIZE, cb)
        conn = self.default_client.connect(self.server)
        conn.negotiate()
        self.assertTrue(callback_future.result(timeout=2))

    def test_post_deserialize(self):
        callback_future = model.Future()
        def cb(frame):
            with callback_future:
                self.assertTrue(isinstance(frame, core.Frame))
                self.assertTrue(isinstance(frame[0], smb2.Smb2))
                self.assertTrue(isinstance(frame[0][0], smb2.NegotiateResponse))
                self.assertTrue(hasattr(frame, "buf"))
                self.assertEqual(frame.len + 4, len(frame.buf))
                callback_future.complete(True)
        self.default_client.register_callback(model.EV_RES_POST_DESERIALIZE, cb)
        conn = self.default_client.connect(self.server)
        conn.negotiate()
        self.assertTrue(callback_future.result(timeout=2))
